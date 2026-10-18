import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk, Gio
from gettext import gettext as _

from numo.core.core_settings import RESOURCE_PATH_PREFIX
from numo.core.settings_manager import SettingsManager
from numo.core.ui_constants import DIFF_ORDER


@Gtk.Template(resource_path=f"{RESOURCE_PATH_PREFIX}/ui/settings.ui")
class NumoSettingsWindow(Adw.PreferencesDialog):
    __gtype_name__ = "NumoSettingsWindow"

    difficulty_row = Gtk.Template.Child()
    timer_minutes_row = Gtk.Template.Child()
    bonus_start_row = Gtk.Template.Child()
    bonus_seconds_row = Gtk.Template.Child()
    tasks_count_row = Gtk.Template.Child()
    recent_sessions_row = Gtk.Template.Child()

    custom_help_button = Gtk.Template.Child()

    custom_add = Gtk.Template.Child()
    custom_add_min = Gtk.Template.Child()
    custom_add_max = Gtk.Template.Child()

    custom_sub = Gtk.Template.Child()
    custom_sub_min = Gtk.Template.Child()
    custom_sub_max = Gtk.Template.Child()
    custom_sub_non_negative = Gtk.Template.Child()

    custom_mul = Gtk.Template.Child()
    custom_mul_min = Gtk.Template.Child()
    custom_mul_max = Gtk.Template.Child()

    custom_div = Gtk.Template.Child()
    custom_div_min = Gtk.Template.Child()
    custom_div_max = Gtk.Template.Child()

    custom_intdiv = Gtk.Template.Child()
    custom_intdiv_min = Gtk.Template.Child()
    custom_intdiv_max = Gtk.Template.Child()

    custom_mod = Gtk.Template.Child()
    custom_mod_min = Gtk.Template.Child()
    custom_mod_max = Gtk.Template.Child()

    custom_reset_row = Gtk.Template.Child()

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
        self._gio.bind("recent-sessions", self.recent_sessions_row, "value", Gio.SettingsBindFlags.DEFAULT)

        self.custom_help_button.connect("clicked", self._on_custom_help_clicked)
        self.custom_reset_row.connect("activated", self._on_custom_reset_activated)

        self._gio.bind("custom-add-enabled", self.custom_add, "enable-expansion", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-sub-enabled", self.custom_sub, "enable-expansion", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-mul-enabled", self.custom_mul, "enable-expansion", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-div-enabled", self.custom_div, "enable-expansion", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-intdiv-enabled", self.custom_intdiv, "enable-expansion", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-mod-enabled", self.custom_mod, "enable-expansion", Gio.SettingsBindFlags.DEFAULT)

        self._gio.bind("custom-sub-non-negative", self.custom_sub_non_negative, "active", Gio.SettingsBindFlags.DEFAULT)

        self._gio.bind("custom-add-min", self.custom_add_min, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-add-max", self.custom_add_max, "value", Gio.SettingsBindFlags.DEFAULT)

        self._gio.bind("custom-sub-min", self.custom_sub_min, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-sub-max", self.custom_sub_max, "value", Gio.SettingsBindFlags.DEFAULT)

        self._gio.bind("custom-mul-min", self.custom_mul_min, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-mul-max", self.custom_mul_max, "value", Gio.SettingsBindFlags.DEFAULT)

        self._gio.bind("custom-div-min", self.custom_div_min, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-div-max", self.custom_div_max, "value", Gio.SettingsBindFlags.DEFAULT)

        self._gio.bind("custom-intdiv-min", self.custom_intdiv_min, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-intdiv-max", self.custom_intdiv_max, "value", Gio.SettingsBindFlags.DEFAULT)

        self._gio.bind("custom-mod-min", self.custom_mod_min, "value", Gio.SettingsBindFlags.DEFAULT)
        self._gio.bind("custom-mod-max", self.custom_mod_max, "value", Gio.SettingsBindFlags.DEFAULT)

        self._gio.connect("changed", self._on_custom_settings_changed)

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

    def _on_custom_help_clicked(self, _button) -> None:
        dialog = Adw.AlertDialog(heading=_("About custom difficulty"))

        label = Gtk.Label(
            label=_(
                "• Division is always performed exactly\n"
                "• Zero is not used as factors or divisors\n"
                "• Integer division and modulo only work with positive divisors\n"
                "• The minimum range of values is five (for example, 0...5)\n"
                "• At least one operation must be enabled"
            ),
            xalign=0,
            wrap=True,
        )

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(label)
        dialog.set_extra_child(box)

        dialog.add_response("close", _("Close"))
        dialog.set_default_response("close")
        dialog.set_close_response("close")
        dialog.present(self)

    def _on_custom_reset_activated(self, _row) -> None:
        dialog = Adw.AlertDialog(
            heading=_("Reset custom difficulty?"),
            body=_("All ranges and operations will be reset to the Medium preset!"),
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("reset", _("Reset"))
        dialog.set_response_appearance(
            "reset", Adw.ResponseAppearance.DESTRUCTIVE
        )
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        dialog.connect("response", self._on_custom_reset_response)
        dialog.present(self)

    def _on_custom_reset_response(self, _dialog: Adw.AlertDialog, response: str) -> None:
        if response != "reset":
            return
        self._settings.reset_custom_to_medium()
        self.show_toast(_("Custom difficulty reset to Medium"))

    def _on_custom_settings_changed(self, _settings, key: str) -> None:
        if key.startswith("custom-"):
            self._settings.update_custom_difficulty()

    def show_toast(self, message: str, timeout: int = 3) -> None:
        toast = Adw.Toast(title=message)
        toast.set_timeout(timeout)
        self.add_toast(toast)
