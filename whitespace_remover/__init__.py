# -*- coding: utf-8 -*-
#
# Whitespace Remover - gedit plugin
# Copyright (C) 2010-2014 Christian Luginbühl
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This software is heavily inspried and in parts based on Osmo Salomaa's
# trailsave plugin <http://users.tkk.fi/~otsaloma/gedit/>.

from gi.repository import GObject, Gedit, PeasGtk

from .config_dialog import ConfigDialog
from .config_settings import ConfigSettings
from .document_manipulator import DocumentManipulator

class WhitespaceRemoverWindowActivatable(GObject.Object,
                                         Gedit.WindowActivatable,
                                         PeasGtk.Configurable):
    """Window hook for whitespace remover plugin."""

    __gtype_name__ = "WhitespeceRemoverWindowActivatable"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        """Constructor."""
        GObject.Object.__init__(self)
        self._config = ConfigSettings()

    def do_activate(self):
        """Callback upon window creation."""
        pass

    def do_deactivate(self):
        """Callback upon window destruction."""
        pass

    def do_update_state(self):
        """Callback upon window state changes."""
        pass

    def do_create_configure_widget(self):
        """Hook for a configuration dialog."""
        return ConfigDialog(self._config)

class WhitespaceRemoverViewActivatable(GObject.Object,
                                       Gedit.ViewActivatable):
    """View hook for whitespace remover plugin."""

    __gtype_name__ = "WhitespaceRemoverViewActivatable"

    view = GObject.property(type=Gedit.View)

    def __init__(self):
        """Constructor."""
        GObject.Object.__init__(self)
        self._config = ConfigSettings()

    def do_activate(self):
        """Callback upon view creation."""
        self._document = self.view.get_buffer()
        self._handler_id = self._document.connect('save', self._on_save)

    def do_deactivate(self):
        """Callback upon view destruction."""
        self._document.disconnect(self._handler_id)

    def do_update_state(self):
        """Callback upon view state changes."""
        pass

    def _on_save(self, *args):
        """Document save handler"""
        self._document.begin_user_action()

        preserve_cursor = self._config.get_bool('preserve-cursor')

        if (self._config.get_bool('remove-whitespace')):
            DocumentManipulator.strip_trailing_spaces_on_lines(self._document,
                                                               preserve_cursor)

        if (self._config.get_bool('remove-newlines')):
            DocumentManipulator.strip_trailing_blank_lines(self._document,
                                                           preserve_cursor)

        self._document.end_user_action()
