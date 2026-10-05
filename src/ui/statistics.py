import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gio", "2.0")

from datetime import datetime
from gettext import gettext as _

from gi.repository import Adw, Gtk, Gio, GLib

from numo.core.core_settings import GameMode, Difficulty, RESOURCE_PATH_PREFIX
from numo.core.custom_errors import StatsError
from numo.utils.stats_manager import StatsManager
from numo.core.ui_constants import (
    MODE_LABELS,
    DIFF_LABELS,
    MODE_ICONS,
    MODE_COLORS,
    ACC_PERCENTAGE_SUCCESS,
    ACC_PERCENTAGE_WARNING,
    NUMBER_OF_RECENT_GAMES
)


@Gtk.Template(resource_path=f"{RESOURCE_PATH_PREFIX}/ui/statistics.ui")
class NumoStatsWindow(Adw.Dialog):
    __gtype_name__ = "NumoStatsWindow"

    toast_overlay = Gtk.Template.Child()

    sessions_label = Gtk.Template.Child()
    game_time_label = Gtk.Template.Child()
    avg_solve_label = Gtk.Template.Child()
    solved_label = Gtk.Template.Child()
    failed_label = Gtk.Template.Child()
    accuracy_label = Gtk.Template.Child()
    accuracy_icon = Gtk.Template.Child()

    best_normal_easy = Gtk.Template.Child()
    best_normal_medium = Gtk.Template.Child()
    best_normal_hard = Gtk.Template.Child()

    best_timer_easy = Gtk.Template.Child()
    best_timer_medium = Gtk.Template.Child()
    best_timer_hard = Gtk.Template.Child()

    best_bonus_easy = Gtk.Template.Child()
    best_bonus_medium = Gtk.Template.Child()
    best_bonus_hard = Gtk.Template.Child()

    best_tasks_easy = Gtk.Template.Child()
    best_tasks_medium = Gtk.Template.Child()
    best_tasks_hard = Gtk.Template.Child()

    recent_list = Gtk.Template.Child()

    export_stats_row = Gtk.Template.Child()
    import_stats_row = Gtk.Template.Child()
    delete_stats_row = Gtk.Template.Child()


    def __init__(self, stats_manager: StatsManager, **kwargs):
        super().__init__(**kwargs)
        self._stats = stats_manager

        self.delete_stats_row.connect("activated", self._on_delete_activated)
        self.export_stats_row.connect("activated", self._on_export_activated)
        self.import_stats_row.connect("activated", self._on_import_activated)

        self._populate()

    def show_toast(self, message: str) -> None:
        toast = Adw.Toast(title=message)
        self.toast_overlay.add_toast(toast)

    def _populate(self) -> None:
        self._populate_overview()
        self._populate_best()
        self._populate_recent()

    def _populate_overview(self) -> None:
        overview = self._stats.overview()
        self.sessions_label.set_label(str(overview["sessions"]))
        self.game_time_label.set_label(self._format_duration_with_hours(overview["total_time"]))
        self.avg_solve_label.set_label(self._format_duration(overview["time_to_task"]))
        self.solved_label.set_label(str(overview["correct"]))
        self.failed_label.set_label(str(overview["wrong"]))

        self._populate_accuracy(overview["accuracy"])

    def _populate_accuracy(self, accuracy: float | None) -> None:
        for css in ("success", "warning", "error", "dim-label"):
            self.accuracy_label.remove_css_class(css)
            self.accuracy_icon.remove_css_class(css)

        if accuracy is None:
            self.accuracy_label.set_label("—")
            self.accuracy_label.add_css_class("dim-label")
            self.accuracy_icon.add_css_class("dim-label")
            return

        self.accuracy_label.set_label(f"{accuracy}%")

        if accuracy >= ACC_PERCENTAGE_SUCCESS:
            color = "success"
        elif accuracy >= ACC_PERCENTAGE_WARNING:
            color = "warning"
        else:
            color = "error"

        self.accuracy_label.add_css_class(color)
        self.accuracy_icon.add_css_class(color)


    def _populate_best(self) -> None:
        best = self._best_sessions()

        self._fill_best_group(
            best[GameMode.NORMAL],
            self.best_normal_easy,
            self.best_normal_medium,
            self.best_normal_hard,
        )
        self._fill_best_group(
            best[GameMode.TIMER],
            self.best_timer_easy,
            self.best_timer_medium,
            self.best_timer_hard,
        )
        self._fill_best_group(
            best[GameMode.TIMER_BONUS],
            self.best_bonus_easy,
            self.best_bonus_medium,
            self.best_bonus_hard,
        )
        self._fill_best_group(
            best[GameMode.TASKS],
            self.best_tasks_easy,
            self.best_tasks_medium,
            self.best_tasks_hard,
        )

    def _best_sessions(self) -> dict:
        result = {mode: {diff: None for diff in Difficulty} for mode in GameMode}
        for s in self._stats.get_sessions():
            current = result[s.mode][s.difficulty]
            if current is None or s.correct > current.correct:
                result[s.mode][s.difficulty] = s
        return result

    def _fill_best_group(self, mode_best, easy_lbl, medium_lbl, hard_lbl) -> None:
        easy_lbl.set_label(self._format_best_session(mode_best[Difficulty.EASY]))
        medium_lbl.set_label(self._format_best_session(mode_best[Difficulty.MEDIUM]))
        hard_lbl.set_label(self._format_best_session(mode_best[Difficulty.HARD]))

    def _populate_recent(self) -> None:
        self.recent_list.remove_all()
        sessions = self._stats.recent(NUMBER_OF_RECENT_GAMES)
        if not sessions:
            row = Adw.ActionRow(
                title=_("No sessions yet"),
                subtitle=_("Play a game to see statistics here"),
            )
            self.recent_list.append(row)
            return

        for s in sessions:
            row = self._format_recent_sessions(s)
            self.recent_list.append(row)

        if len(sessions) < NUMBER_OF_RECENT_GAMES:
            row = Adw.ActionRow(
                title=_("No more sessions"),
                subtitle=_("You have fewer than %d recorded sessions") % NUMBER_OF_RECENT_GAMES,
            )
            self.recent_list.append(row)

    def _format_recent_sessions(self, s) -> Adw.ActionRow:
        row = Adw.ActionRow(
            title=self._format_timestamp(s.dt),
            subtitle=f"{MODE_LABELS[s.mode]} · {DIFF_LABELS[s.difficulty]}",
        )

        icon = Gtk.Image.new_from_icon_name(MODE_ICONS[s.mode])
        icon.add_css_class(MODE_COLORS[s.mode])
        row.add_prefix(icon)

        row.add_suffix(Gtk.Label(
            label=self._format_session_summary(s),
            css_classes=["dim-label", "numeric"],
        ))

        return row

    def _format_best_session(self, s) -> str:
        if s is None:
            return "—"
        return self._format_session_summary(s)

    def _format_session_summary(self, s) -> str:
        duration = self._format_duration(s.elapsed_sec)
        if s.accuracy is None:
            return f"0 · 0% · {duration}"
        return f"{s.correct} · {s.accuracy}% · {duration}"

    @staticmethod
    def _format_duration(seconds: float) -> str:
        total = int(seconds)
        minutes, secs = divmod(total, 60)
        return f"{minutes}:{secs:02d}"

    @staticmethod
    def _format_duration_with_hours(seconds: float) -> str:
        total = int(seconds)
        hours, remainder = divmod(total, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours}:{minutes:02d}:{secs:02d}"

    @staticmethod
    def _format_timestamp(dt: datetime) -> str:
        now = datetime.now()
        if dt.date() == now.date():
            return dt.strftime(_("Today %H:%M"))
        return dt.strftime("%Y-%m-%d %H:%M")

    def _on_delete_activated(self, _row):
        dialog = Adw.AlertDialog(
            heading=_("Delete all statistics?"),
            body=_("This action cannot be undone."),
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("delete", _("Delete"))
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        dialog.connect("response", self._on_delete_response)
        dialog.present(self)

    def _on_delete_response(self, _dialog, response):
        if response != "delete":
            return

        try:
            self._stats.clear()
        except StatsError as e:
            self.show_toast(str(e))
            return
        self._populate()

    def _on_export_activated(self, _row):
        dialog = self._create_json_file_dialog(
            title=_("Export statistics"),
            initial_name="stats.json",
        )
        dialog.save(self.get_root(), None, self._on_export_finish)

    def _on_export_finish(self, dialog, result):
        file = self._finish_file_dialog(dialog.save_finish, result)
        if file is None:
            return
        try:
            self._stats.export_to(file)
            self.show_toast(_("Statistics exported"))
        except StatsError as e:
            self.show_toast(str(e))

    def _on_import_activated(self, _row):
        dialog = self._create_json_file_dialog(
            title=_("Import statistics"),
        )
        dialog.open(self.get_root(), None, self._on_import_finish)

    def _on_import_finish(self, dialog, result):
        file = self._finish_file_dialog(dialog.open_finish, result)
        if file is None:
            return
        try:
            self._stats.import_from(file)
            self.show_toast(_("Statistics imported"))
        except StatsError as e:
            self.show_toast(str(e))
            return
        self._populate()


    def _create_json_file_dialog(self, title, initial_name=None):
        dialog = Gtk.FileDialog()
        dialog.set_title(title)

        if initial_name is not None:
            dialog.set_initial_name(initial_name)

        json_filter = self._create_json_filter()
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(json_filter)

        dialog.set_filters(filters)
        dialog.set_default_filter(json_filter)

        return dialog

    @staticmethod
    def _finish_file_dialog(finish_func, result):
        try:
            return finish_func(result)
        except GLib.Error:
            return None

    @staticmethod
    def _create_json_filter():
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("JSON files"))
        file_filter.add_mime_type("application/json")
        file_filter.add_pattern("*.json")
        return file_filter
