import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk, Gio

from numo.core.core_settings import RESOURCE_PATH_PREFIX
from numo.core.settings_manager import SettingsManager
from numo.core.ui_constants import DIFF_ORDER


@Gtk.Template(resource_path=f"{RESOURCE_PATH_PREFIX}/ui/settings.ui")
class NumoSettingsWindow(Adw.PreferencesDialog):
    __gtype_name__ = "NumoSettingsWindow"

    difficulty_row     = Gtk.Template.Child()
    timer_minutes_row  = Gtk.Template.Child()
    bonus_start_row    = Gtk.Template.Child()
    bonus_seconds_row  = Gtk.Template.Child()
    tasks_count_row    = Gtk.Template.Child()

    def __init__(self, settings: SettingsManager, **kwargs):
        super().__init__(**kwargs)
        self._settings = settings
        self._gio = settings.settings

        self._sync_difficulty_from_settings()

        self.difficulty_row.connect("notify::selected", self._on_difficulty_changed)

        self._gio.connect("changed::difficulty", self._on_difficulty_settings_changed)

        self._gio.bind("timer-duration-min", self.timer_minutes_row, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("bonus-initial-sec", self.bonus_start_row, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("bonus-per-correct-sec", self.bonus_seconds_row, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("tasks-count", self.tasks_count_row, "value", Gio.SettingsBindFlags.DEFAULT)


    def _sync_difficulty_from_settings(self):
        nick = self._gio.get_string("difficulty")
        index = DIFF_ORDER.index(nick) if nick in DIFF_ORDER else 0
        self.difficulty_row.set_selected(index)

    def _on_difficulty_changed(self, row, _pspec):
        index = row.get_selected()
        if 0 <= index < len(DIFF_ORDER):
            self._gio.set_string("difficulty", DIFF_ORDER[index])

    def _on_difficulty_settings_changed(self, _settings, _key):
        self._sync_difficulty_from_settings()
