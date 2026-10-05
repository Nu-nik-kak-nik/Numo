# main.py
#
# Copyright 2026 Nu-nik-kak-nik
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

import sys
import gi

from gettext import gettext as _

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version("Gdk", "4.0")

from gi.repository import Gdk, Gtk, Gio, Adw

from .ui.window import NumoWindow
from .ui.settings import NumoSettingsWindow
from .ui.statistics import NumoStatsWindow

from numo.core.core_settings import APP_VERSION
from numo.core.settings_manager import SettingsManager
from numo.utils.stats_manager import StatsManager


class NumoApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.Nu_nik_kak_nik.Numo',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/io/github/Nu_nik_kak_nik/Numo')
        self.settings = SettingsManager()
        self.stats_manager = StatsManager(
            app_version=APP_VERSION,
            on_warning=self._on_stats_warning,
        )
        self._setup_actions()
        self._load_css()
        self.window = None

    def _setup_actions(self):
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action, ['F1'])
        self.create_action('preferences', self.on_preferences_action, ['<primary>comma'])
        self.create_action('statistics', self.on_statistics_action, ['<primary>s'])
        self.create_action('shortcuts', self.on_shortcuts_action, ['<primary>question'])

    def _load_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_resource("/io/github/Nu_nik_kak_nik/Numo/ui/style.css")
        display = Gdk.Display.get_default()
        if display is not None:
            Gtk.StyleContext.add_provider_for_display(
                display,
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )

    def _load_icons(self):
        display = Gdk.Display.get_default()
        theme = Gtk.IconTheme.get_for_display(display)
        theme.add_resource_path("/io/github/Nu_nik_kak_nik/Numo/icons")

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.window = self.props.active_window
        if not self.window:
            self.window = NumoWindow(
            settings=self.settings,
            stats_manager=self.stats_manager,
            application=self,
        )
        self.window.present()

        try:
            self.stats_manager.load()
        except StatsError:
            pass

    def on_preferences_action(self, _action, _param):
        for win in self.get_windows():
            if isinstance(win, NumoSettingsWindow):
                win.present(self.window)
                return None
        win = NumoSettingsWindow(settings=self.settings)
        win.present(self.window)

    def on_statistics_action(self, _action, _param):
        for win in self.get_windows():
            if isinstance(win, NumoStatsWindow):
                win.present(self.window)
                return None
        win = NumoStatsWindow(stats_manager=self.stats_manager, settings=self.settings)
        win.present(self.window)

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog.new_from_appdata(
        "/io/github/Nu_nik_kak_nik/Numo/io.github.Nu_nik_kak_nik.Numo.metainfo.xml",
        APP_VERSION,
        )
        about.set_copyright("© 2026 Nu-nik-kak-nik")
        about.set_translator_credits(_("translator-credits"))
        about.add_credit_section(
            _("Code author"),
            ["Nu-nik-kak-nik https://github.com/Nu-nik-kak-nik"],
        )
        about.present(self.props.active_window)

    def on_shortcuts_action(self, *args):
        builder = Gtk.Builder.new_from_resource(
            '/io/github/Nu_nik_kak_nik/Numo/ui/shortcuts-dialog.ui'
        )
        dialog = builder.get_object('shortcuts_dialog')
        dialog.present(self.window)

    def _on_stats_warning(self, message: str) -> None:
        for win in self.get_windows():
            if isinstance(win, NumoStatsWindow) and win.get_visible():
                win.show_toast(message)
                return
        if self.window is not None and hasattr(self.window, "show_toast"):
            self.window.show_toast(message)


def main(version):
    """The application's entry point."""
    app = NumoApplication()
    return app.run(sys.argv)
