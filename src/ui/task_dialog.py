import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gettext import gettext as _
from dataclasses import dataclass

from gi.repository import Adw, Gtk

from numo.core.core_settings import RESOURCE_PATH_PREFIX, TaskRecord
from numo.core.ui_constants import MAX_TASK_RECORDS
from numo.utils.toast_builder import ToastMixin


@Gtk.Template(resource_path=f"{RESOURCE_PATH_PREFIX}/ui/task_dialog.ui")
class NumoTasksStatsDialog(Adw.Dialog, ToastMixin):
    __gtype_name__ = "NumoTasksStatsDialog"

    toast_overlay = Gtk.Template.Child()

    tasks_list = Gtk.Template.Child()
    content_stack = Gtk.Template.Child()
    correct_toggle = Gtk.Template.Child()
    wrong_toggle = Gtk.Template.Child()
    list_page = Gtk.Template.Child()
    empty_page = Gtk.Template.Child()

    def __init__(self, records: list[TaskRecord] | None = None, **kwargs):
        super().__init__(**kwargs)
        self._records = records or []

        if len(self._records) >= MAX_TASK_RECORDS:
            self.show_toast(_("Record limit reached"))

        self.correct_toggle.connect("toggled", self._on_filter_changed)
        self.wrong_toggle.connect("toggled", self._on_filter_changed)

        self._populate_list()
        self.tasks_list.set_filter_func(self._filter_row)
        self._on_filter_changed()

    def _add_toast(self, toast: Adw.Toast) -> None:
        self.toast_overlay.add_toast(toast)

    def _populate_list(self):
        for record in self._records[:MAX_TASK_RECORDS]:
            self.tasks_list.append(self._create_row(record))

    def _create_row(self, record: TaskRecord) -> Adw.ActionRow:
        row = Adw.ActionRow()
        row.set_title(f"{record.expression} = {record.user_answer}")

        number_label = Gtk.Label(label=f"{record.number}.")
        number_label.add_css_class("heading")
        number_label.add_css_class("numeric")
        row.add_prefix(number_label)

        suffix_box = Gtk.Box(spacing=8, valign=Gtk.Align.CENTER)
        time_label = Gtk.Label(
            label=_("%(time_seconds)d s") % {"time_seconds": record.time_seconds}
        )
        time_label.add_css_class("dimmed")
        time_label.add_css_class("caption")
        suffix_box.append(time_label)
        icon = Gtk.Image.new_from_icon_name(
            "object-select-symbolic" if record.is_correct else "cross-symbolic"
        )
        suffix_box.append(icon)

        row.add_suffix(suffix_box)
        row.add_css_class("success-bg" if record.is_correct else "error-bg")
        row._is_correct = record.is_correct
        return row

    def _filter_row(self, row: Gtk.ListBoxRow) -> bool:
        is_correct = getattr(row, "_is_correct", False)
        if is_correct:
            return self.correct_toggle.get_active()
        return self.wrong_toggle.get_active()

    def _on_filter_changed(self, *_):
        self.tasks_list.invalidate_filter()
        if not self.correct_toggle.get_active() and not self.wrong_toggle.get_active():
            self.content_stack.set_visible_child(self.empty_page)
        else:
            self.content_stack.set_visible_child(self.list_page)
