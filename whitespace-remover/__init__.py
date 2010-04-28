# -*- coding: utf-8 -*-
#
# Whitespace Remover - gedit plugin
# Copyright (C) 2010 Christian Luginbühl
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

import gedit

from config_dialog import ConfigDialog
from config_settings import ConfigSettings
from document_manipulator import DocumentManipulator

class WhitespaceRemoverPlugin(gedit.Plugin):
    """Automatically strip all trailing whitespace upon saving."""

    def __init__(self):
        """Constructor."""
        self._config = ConfigSettings()

    def activate(self, window):
        """Activate plugin."""

        handler_id = window.connect("tab-added", self.on_window_tab_added)
        window.set_data(self.__class__.__name__, handler_id)
        for doc in window.get_documents():
            self.connect_document(doc)

    def connect_document(self, doc):
        """Connect to document's 'saving' signal."""

        handler_id = doc.connect("saving", self.on_document_saving)
        doc.set_data(self.__class__.__name__, handler_id)

    def deactivate(self, window):
        """Deactivate plugin."""

        name = self.__class__.__name__
        handler_id = window.get_data(name)
        window.disconnect(handler_id)
        window.set_data(name, None)
        for doc in window.get_documents():
            handler_id = doc.get_data(name)
            doc.disconnect(handler_id)
            doc.set_data(name, None)

    def ui_update(self, window):
        """Update the user-interface."""
        pass

    def is_configurable(self):
        """Returns that this plugin is configurable."""
        return True

    def create_configure_dialog(self):
        """Show the plugin settings window."""
        dialog = ConfigDialog(self, self._config)
        return dialog

    def on_window_tab_added(self, window, tab):
        """Connect the document in tab."""

        name = self.__class__.__name__
        doc = tab.get_document()
        handler_id = doc.get_data(name)
        if handler_id is None:
            self.connect_document(doc)

    def on_document_saving(self, doc, *args):
        """Strip trailing spaces in document."""

        doc.begin_user_action()
        if (self._config.get_bool('remove_whitespace')):
            DocumentManipulator.strip_trailing_spaces_on_lines(doc)

        if (self._config.get_bool('remove_newlines')):
            DocumentManipulator.strip_trailing_blank_lines(doc)

        doc.end_user_action()
