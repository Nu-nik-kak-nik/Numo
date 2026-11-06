from gettext import gettext as _

from gi.repository import Adw, Gtk

from numo.core.custom_errors import StatsError
from numo.core.ui_constants import stats_error_message
from numo.ui.error_dialog import NumoErrorDialog


class ToastMixin:
    @staticmethod
    def _build_toast(message: str, timeout: int = 3) -> Adw.Toast:
        toast = Adw.Toast(title=message)
        toast.set_timeout(timeout)
        return toast

    def _add_toast(self, toast: Adw.Toast) -> None:
        """subclasses must override this method"""
        raise NotImplementedError

    def show_toast(self, message: str, timeout: int = 3) -> None:
        self._add_toast(self._build_toast(message, timeout))

    def show_detailed_toast(
        self,
        message: str,
        details: str,
        timeout: int = 5
    ) -> Adw.Toast:
        toast = self._build_toast(message, timeout)
        toast.set_button_label(_("Details"))
        toast.connect("button-clicked", self._on_details_clicked, message, details)
        self._add_toast(toast)

    def _on_details_clicked(
        self,
        _toast: Adw.Toast,
        message: str,
        details: str
    ) -> None:
        dialog = NumoErrorDialog(short_message=message, details=details)
        dialog.present(self)

    def show_stats_error(self, error: StatsError) -> None:
        message = stats_error_message(error)
        details = f"{error.code}: {error.details}" if error.details else error.code
        self.show_detailed_toast(message, details)
