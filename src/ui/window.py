# window.py
#
# Copyright 2026 lis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gettext import gettext as _

from gi.repository import Adw, Gtk, GLib, Gdk

from numo.core.core_settings import GameMode, Difficulty
from numo.core.custom_errors import StatsError
from numo.core.settings_manager import SettingsManager
from numo.game.game_session import GameSession
from numo.utils.stats_manager import StatsManager
from numo.core.ui_constants import (
TICK_INTERVAL_MS,
FEEDBACK_DURATION_MS,
BONUS_FADE_MS,
MODE_ICONS,
MODE_COLORS,
MODE_LABELS,
DIFFICULTY_LABELS,
DIFFICULTY_ICONS
)


@Gtk.Template(resource_path='/org/gnome/Example/ui/window.ui')
class NumoWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'NumoWindow'

    toast_overlay = Gtk.Template.Child()
    nav_view = Gtk.Template.Child()

    expression_label = Gtk.Template.Child()
    answer_entry = Gtk.Template.Child()
    submit_button = Gtk.Template.Child()
    status_label = Gtk.Template.Child()
    bonus_label = Gtk.Template.Child()

    mode_normal = Gtk.Template.Child()
    mode_timer = Gtk.Template.Child()
    mode_timer_bonus = Gtk.Template.Child()
    mode_tasks = Gtk.Template.Child()

    game_back_button = Gtk.Template.Child()

    results_value_accuracy = Gtk.Template.Child()
    results_value_time = Gtk.Template.Child()
    results_value_correct = Gtk.Template.Child()
    results_value_wrong = Gtk.Template.Child()

    results_icon_mode = Gtk.Template.Child()
    results_label_mode = Gtk.Template.Child()
    results_icon_difficulty = Gtk.Template.Child()
    results_label_difficulty = Gtk.Template.Child()
    results_icon_extra = Gtk.Template.Child()
    results_label_extra = Gtk.Template.Child()
    results_big_icon = Gtk.Template.Child()

    results_ok_button = Gtk.Template.Child()

    def __init__(self, settings: SettingsManager,
                 stats_manager: StatsManager, **kwargs):
        super().__init__(**kwargs)
        self._settings = settings
        self._stats = stats_manager

        self._session: GameSession | None = None
        self._tick_source: int | None = None
        self._finished = False

        self._game_key_controller = None
        self._results_key_controller = None

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.mode_normal.connect("activated", lambda *_: self._start_game(GameMode.NORMAL))
        self.mode_timer.connect("activated", lambda *_: self._start_game(GameMode.TIMER))
        self.mode_timer_bonus.connect("activated", lambda *_: self._start_game(GameMode.TIMER_BONUS))
        self.mode_tasks.connect("activated", lambda *_: self._start_game(GameMode.TASKS))

        self.game_back_button.connect("clicked", self._on_game_back_clicked)
        self.submit_button.connect("clicked", self._on_submit_clicked)
        self.results_ok_button.connect("clicked", self._on_results_ok_clicked)

        self.answer_entry.connect("activate", self._on_answer_activated)
        self.answer_entry.set_max_length(7)

        self._key_controller = Gtk.EventControllerKey.new()
        self._key_controller.connect("key-pressed", self._on_key_pressed)
        self.add_controller(self._key_controller)


    def _on_key_pressed(self, controller, keyval, keycode, state):
        page = self.nav_view.get_visible_page()
        if page is None:
            return False
        tag = page.get_tag()

        if tag == "game" and keyval == Gdk.KEY_Escape:
            self._on_game_back_clicked(None)
            return True

        if tag == "results" and keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            self._on_results_ok_clicked(None)
            return True

        return False

    def show_toast(self, message: str, timeout: int = 5) -> None:
        toast = Adw.Toast(title=message)
        toast.set_timeout(timeout)
        self.toast_overlay.add_toast(toast)

    def _start_game(self, mode: GameMode) -> None:
        difficulty = self._settings.get_difficulty()
        options = self._settings.session_options_for(mode)

        self._session = GameSession(mode, difficulty, options)
        self._finished = False
        self._reset_status_label_style()

        page = self.nav_view.find_page("game")
        self.nav_view.push(page)
        self._show_current_task()

        if mode in (GameMode.TIMER, GameMode.TIMER_BONUS):
            self._tick_source = GLib.timeout_add(TICK_INTERVAL_MS, self._on_tick)

    def _reset_status_label_style(self) -> None:
        self.status_label.remove_css_class("error")
        if "dim-label" not in self.status_label.get_css_classes():
            self.status_label.add_css_class("dim-label")

    def _show_current_task(self) -> None:
        task = self._session.current_task
        self.expression_label.set_label(f"{task.expression} = ?")
        self.status_label.set_label(self._session.status_text())
        self.answer_entry.set_text("")
        self.answer_entry.set_sensitive(True)
        self.submit_button.set_sensitive(True)
        GLib.idle_add(self._focus_entry)

    def _focus_entry(self) -> bool:
        self.answer_entry.grab_focus()
        return False

    def _on_answer_activated(self, _entry) -> None:
        self._submit_current()

    def _on_submit_clicked(self, _row) -> None:
        self._submit_current()

    def _submit_current(self) -> None:
        if self._session is None:
            self.show_toast(_("No active game."), 1)
            return
        if  self._finished:
            self.show_toast(_("The game is already over."), 1)
            return

        text = self.answer_entry.get_text().strip()
        if not text:
            self.show_toast(_("Please enter an answer."), 1)
            return

        try:
            value = int(text)
        except ValueError:
            self.show_toast(_("Please enter a integer."), 1)
            return
        self._submit_answer(value)

    def _deactivate_entry(self) -> bool:
        if self._session is not None:
            self.answer_entry.set_sensitive(False)
            self.submit_button.set_sensitive(False)
        return False

    def _submit_answer(self, value: int) -> None:
        GLib.idle_add(self._deactivate_entry)
        is_correct = self._session.submit(value)
        self._flash_feedback(is_correct)

    def _flash_feedback(self, is_correct: bool) -> None:
        css_class = "success" if is_correct else "error"
        self.expression_label.add_css_class(css_class)

        show_bonus = (
            is_correct
            and self._session.mode == GameMode.TIMER_BONUS
        )
        if show_bonus:
            bonus = self._session._options.bonus_sec or 0
            self.bonus_label.set_opacity(1.0)
            self.bonus_label.set_label(f"+{bonus} s")

        def restore():
            self.expression_label.remove_css_class(css_class)
            if show_bonus:
                self._fade_out_bonus()
            if self._finished:
                return False
            if self._session.finished:
                self._finish_session()
            else:
                self._show_current_task()
            return False

        GLib.timeout_add(FEEDBACK_DURATION_MS, restore)

    def _fade_out_bonus(self) -> None:
        target = Adw.PropertyAnimationTarget.new(self.bonus_label, "opacity")
        anim = Adw.TimedAnimation.new(
            self.bonus_label,
            1.0,
            0.0,
            BONUS_FADE_MS,
            target,
        )
        anim.set_easing(Adw.Easing.EASE_OUT_CUBIC)
        anim.connect("done", lambda *_: self._clear_bonus_label())
        anim.play()


    def _clear_bonus_label(self) -> bool:
        self.bonus_label.set_label("")
        self.bonus_label.set_opacity(1.0)
        return False

    def _on_tick(self) -> bool:
        if self._finished or self._session is None:
            self._tick_source = None
            return False

        delta = TICK_INTERVAL_MS / 1000.0
        if self._session.tick(delta):
            self._tick_source = None
            self._finish_session()
            return False

        self.status_label.set_label(self._session.status_text())
        self._update_timer_color()
        return True

    def _update_timer_color(self) -> None:
        if self._session.mode not in (GameMode.TIMER, GameMode.TIMER_BONUS):
            return
        time_left = self._session.time_left
        if time_left is not None and time_left <= 10:
            if "error" not in self.status_label.get_css_classes():
                self.status_label.remove_css_class("dim-label")
                self.status_label.add_css_class("error")
        else:
            if "error" in self.status_label.get_css_classes():
                self.status_label.remove_css_class("error")
                self.status_label.add_css_class("dim-label")

    def _finish_session(self) -> None:
        if self._finished:
            return
        self._finished = True

        if self._tick_source is not None:
            GLib.source_remove(self._tick_source)
            self._tick_source = None

        try:
            self._stats.add_session(self._session.to_record())
        except StatsError as e:
            self.show_toast(str(e))

        self._show_results()

    def _show_results(self) -> None:
        s = self._session
        data = s.result_data()

        self.results_big_icon.set_from_icon_name(MODE_ICONS[data["mode"]])

        self.results_value_correct.set_label(str(data["correct"]))
        self.results_value_wrong.set_label(str(data["wrong"]))
        self.results_value_accuracy.set_label(str(data["accuracy"]))
        self.results_value_time.set_label(str(data["duration"]))

        self.results_icon_mode.set_from_icon_name(MODE_ICONS[s.mode])
        self.results_label_mode.set_label(MODE_LABELS[s.mode])
        self.results_icon_difficulty.set_from_icon_name(DIFFICULTY_ICONS[data["difficulty"]])
        self.results_label_difficulty.set_label(DIFFICULTY_LABELS[data["difficulty"]])
        self.results_icon_extra.set_from_icon_name("media-playback-start-symbolic")

        self._populate_end(data)

        page = self.nav_view.find_page("results")
        self.nav_view.push(page)

    def _populate_end(self, data: dict[str, int | float | list[int]]) -> None:
        options = self._session._options

        match data["mode"]:
            case GameMode.NORMAL:
                self.results_label_extra.set_label(
                    _("{count} tasks solved").format(count=data["mode_data"])
                )
            case GameMode.TIMER:
                self.results_label_extra.set_label(
                    _("{minutes} min").format(minutes=data["mode_data"])
                )
            case GameMode.TIMER_BONUS:
                self.results_label_extra.set_label(
                    _("{initial} s + {bonus} s").format(
                        initial=options.initial_time_sec or 0,
                        bonus=options.bonus_sec or 0,
                    )
                )
            case GameMode.TASKS:
                self.results_label_extra.set_label(
                    _("{count} tasks").format(count=data["mode_data"] or 0)
                )

            case _:
                self.results_label_extra.set_label(0)



    def _on_results_ok_clicked(self, _button) -> None:
        self._session = None
        self._finished = False
        self.nav_view.pop_to_tag("home")

    def _on_game_back_clicked(self, _button) -> None:
        if self._session is None or self._finished:
            self._abort_and_home()
            return

        dialog = Adw.AlertDialog(
            heading=_("Interrupt the game?"),
            body=_("Your progress will not be saved."),
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("interrupt", _("Interrupt"))
        dialog.set_response_appearance(
            "interrupt", Adw.ResponseAppearance.DESTRUCTIVE
        )
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        dialog.connect("response", self._on_interrupt_response)
        dialog.present(self)

    def _on_interrupt_response(self, _dialog, response) -> None:
        if response != "interrupt":
            return
        self._abort_and_home()

    def _abort_and_home(self) -> None:
        if self._tick_source is not None:
            GLib.source_remove(self._tick_source)
            self._tick_source = None
        self._session = None
        self._finished = False
        self._reset_status_label_style()
        self.nav_view.pop_to_tag("home")
