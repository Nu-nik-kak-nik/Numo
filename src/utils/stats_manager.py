import json
import os

import gi

gi.require_version("Gio", "2.0")
gi.require_version("GLib", "2.0")

from gi.repository import Gio, GLib

from numo.core.core_settings import (
    GameMode,
    Difficulty,
    SCHEMA_VERSION,
    MAX_SESSIONS,
    STATS_FILENAME,
    APP_DATA_SUBDIR,
    RECENT_GAMES,
)
from numo.core.stats_schema import Session, StatsFile
from numo.core.custom_errors import StatsError


class StatsManager:

    def __init__(self, app_version: str = "", on_warning=None):
        super().__init__()
        self._app_version: str = app_version
        self._on_warning = on_warning
        self._file: Gio.File = self._default_file()
        self._stats: StatsFile = StatsFile(version=SCHEMA_VERSION, app_version=app_version)
        self._mtime: int | None = None

    def _default_file(self) -> Gio.File:
        path = os.path.join(GLib.get_user_data_dir(), APP_DATA_SUBDIR, STATS_FILENAME)
        return Gio.File.new_for_path(path)

    def file(self) -> Gio.File:
        return self._file

    def path(self) -> str:
        return self._file.get_path() or ""

    def _current_mtime(self) -> int | None:
        try:
            info = self._file.query_info(
                "time::modified", Gio.FileQueryInfoFlags.NONE, None
            )
            return info.get_modification_date_time().to_unix()
        except GLib.Error:
            return None

    def load(self) -> None:
        if self.mtime_validation():
            return
        self._load_from_disk()
        self._mtime = self._current_mtime()

    def mtime_validation(self) -> bool:
        mtime = self._current_mtime()
        return bool(mtime is not None and mtime == self._mtime)

    def _load_from_disk(self) -> None:
        if not self._file.query_exists(None):
            self._stats = StatsFile(version=SCHEMA_VERSION, app_version=self._app_version)
            try:
                self._save_internal()
            except StatsError:
                pass
            return

        try:
            ok, contents, _etag = self._file.load_contents(None)
        except GLib.Error as e:
            self._recreate(f"failed to read the statistics file: {e.message}")
            return
        if not ok:
            self._recreate("failed to read the statistics file.")
            return

        try:
            data = json.loads(contents.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._recreate("The statistics file is corrupted. The statistics were dropped.")
            return

        try:
            self._stats = StatsFile.from_dict(data)
            self._stats.app_version = self._app_version
        except (KeyError, ValueError, TypeError):
            self._recreate(
                "Incorrect structure of the statistics file. The statistics were dropped."
            )
            return

    def _recreate(self, message: str) -> None:
        self._stats = StatsFile(version=SCHEMA_VERSION, app_version=self._app_version)
        try:
            self._save_internal()
        except StatsError:
            pass
        if self._on_warning is not None:
            self._on_warning(message)

    def save(self) -> None:
        parent = self._file.get_parent()
        if parent is not None and not parent.query_exists(None):
            try:
                parent.make_directory_with_parents(None)
            except GLib.Error as e:
                if not e.matches(Gio.io_error_quark(), Gio.IOErrorEnum.EXISTS):
                    raise StatsError(f"Failed to create a directory: {e.message}")
        self._save_internal()

    def _save_internal(self) -> None:
        text = json.dumps(self._stats.to_dict(), indent=2, ensure_ascii=False)
        data = text.encode("utf-8")
        try:
            self._file.replace_contents(
                data,
                None,
                False,
                Gio.FileCreateFlags.REPLACE_DESTINATION,
                None,
            )
        except GLib.Error as e:
            raise StatsError(f"The statistics were not kept: {e.message}")
        self._mtime = self._current_mtime()

    def add_session(self, session: Session) -> None:
        self.load()
        self._stats.sessions.append(session)
        self._trim()
        self.save()

    def clear(self) -> None:
        self.load()
        self._stats.sessions.clear()
        self.save()

    def _trim(self) -> None:
        if len(self._stats.sessions) > MAX_SESSIONS:
            self._stats.sessions = self._stats.sessions[-MAX_SESSIONS:]

    def export_to(self, file: Gio.File) -> None:
        self.load()
        text = json.dumps(self._stats.to_dict(), indent=2, ensure_ascii=False)
        data = text.encode("utf-8")
        try:
            file.replace_contents(
                data,
                None,
                False,
                Gio.FileCreateFlags.REPLACE_DESTINATION,
                None,
            )
        except GLib.Error as e:
            raise StatsError(f"Failed to export: {e.message}")

    def import_from(self, file: Gio.File) -> None:
        try:
            ok, contents, _etag = file.load_contents(None)
        except GLib.Error as e:
            raise StatsError(f"File reading error: {e.message}")
        if not ok:
            raise StatsError("File reading error.")

        try:
            data = json.loads(contents.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise StatsError(f"The file is not correct JSON: {e}")

        try:
            new_stats = StatsFile.from_dict(data)
        except (KeyError, ValueError, TypeError) as e:
            raise StatsError(f"Incorrect file structure: {e}")

        new_stats.app_version = self._app_version
        self._stats = new_stats
        self._trim()
        self.save()

    def get_sessions(self) -> list[Session]:
        self.load()
        return list(self._stats.sessions)

    def overview(self) -> dict[str, int | float | None]:
        self.load()
        sessions = self._stats.sessions

        correct = 0
        wrong = 0
        total_time = 0.0

        for s in sessions:
            correct += s.correct
            wrong += s.wrong
            total_time += s.elapsed_sec

        attempts = correct + wrong

        if attempts == 0:
            accuracy = None
            time_to_task = 0

        elif total_time == 0:
            accuracy = round(correct / attempts * 100.0, 1)
            time_to_task = 0

        else:
            accuracy = round(correct / attempts * 100.0, 1)
            time_to_task = round(total_time / attempts, 1)

        return {
            "sessions": len(sessions),
            "correct": correct,
            "wrong": wrong,
            "accuracy": accuracy,
            "total_time": round(total_time, 1),
            "time_to_task": time_to_task,
        }

    def best_results(self) -> dict:
        self.load()
        result = {mode: {diff: 0 for diff in Difficulty} for mode in GameMode}
        for s in self._stats.sessions:
            result[s.mode][s.difficulty] = max(
                result[s.mode][s.difficulty], s.correct
            )
        return result

    def best_overall_for_mode(self, mode: GameMode) -> tuple[int, Difficulty | None]:
        self.load()
        best_value = 0
        best_diff: Difficulty | None = None
        for s in self._stats.sessions:
            if s.mode != mode:
                continue
            if s.correct > best_value:
                best_value = s.correct
                best_diff = s.difficulty
        return best_value, best_diff

    def recent(self, n: int = RECENT_GAMES) -> list[Session]:
        self.load()
        return list(reversed(self._stats.sessions[-n:]))
