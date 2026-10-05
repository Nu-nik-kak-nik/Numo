import gi

gi.require_version("Gio", "2.0")

from gi.repository import Gio, GObject

from numo.core.core_settings import Difficulty, GameMode, SessionOptions, SCHEMA_ID
from numo.core.ui_constants import DIFF_TO_NICK, NICK_TO_DIFF


class SettingsManager:
    def __init__(self):
        self._settings = Gio.Settings.new(SCHEMA_ID)

    @property
    def settings(self) -> Gio.Settings:
        return self._settings

    def get_difficulty(self) -> Difficulty:
        return NICK_TO_DIFF[self._settings.get_string("difficulty")]

    def set_difficulty(self, difficulty: Difficulty) -> None:
        self._settings.set_string("difficulty", DIFF_TO_NICK[difficulty])

    def get_timer_duration_min(self) -> int:
        return self._settings.get_int("timer-duration-min")

    def set_timer_duration_min(self, value: int) -> None:
        self._settings.set_int("timer-duration-min", value)

    def get_bonus_initial_sec(self) -> int:
        return self._settings.get_int("bonus-initial-sec")

    def set_bonus_initial_sec(self, value: int) -> None:
        self._settings.set_int("bonus-initial-sec", value)

    def get_bonus_per_correct_sec(self) -> int:
        return self._settings.get_int("bonus-per-correct-sec")

    def set_bonus_per_correct_sec(self, value: int) -> None:
        self._settings.set_int("bonus-per-correct-sec", value)

    def get_tasks_count(self) -> int:
        return self._settings.get_int("tasks-count")

    def set_tasks_count(self, value: int) -> None:
        self._settings.set_int("tasks-count", value)

    def session_options_for(self, mode: GameMode) -> SessionOptions:
        if mode == GameMode.TIMER:
            return SessionOptions(
                duration_sec=self.get_timer_duration_min() * 60,
            )
        if mode == GameMode.TIMER_BONUS:
            return SessionOptions(
                initial_time_sec=self.get_bonus_initial_sec(),
                bonus_sec=self.get_bonus_per_correct_sec(),
            )
        if mode == GameMode.TASKS:
            return SessionOptions(
                target_tasks=self.get_tasks_count(),
            )
        return SessionOptions()

    def get_recent_sessions(self) -> int:
        return self._settings.get_int("recent-sessions")

    def set_recent_sessions(self, value: int) -> None:
        return self._settings.set_int("recent-sessions", value)

