import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")

from gettext import gettext as _

from gi.repository import Adw, Gdk, Gtk

from numo.core.core_settings import RESOURCE_PATH_PREFIX


@Gtk.Template(resource_path=f"{RESOURCE_PATH_PREFIX}/ui/error_dialog.ui")
class NumoErrorDialog(Adw.Dialog):
    __gtype_name__ = "NumoErrorDialog"

    toast_overlay = Gtk.Template.Child()

    message_label = Gtk.Template.Child()
    details_view = Gtk.Template.Child()
    copy_button = Gtk.Template.Child()

    def __init__(self, short_message: str, details: str, **kwargs):
        super().__init__(**kwargs)
        self._details = details
        self.message_label.set_label(short_message)
        self.details_view.get_buffer().set_text(details)
        self.copy_button.connect("clicked", self._on_copy_clicked)

    def _on_copy_clicked(self, _button) -> None:
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(self._details)

        toast = Adw.Toast(title=_("Copied to clipboard"))
        toast.set_timeout(2)
        self.toast_overlay.add_toast(toast)
