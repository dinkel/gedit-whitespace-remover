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

from document_helper import DocumentHelper

class WindowHelper:
    """Handles a window instance."""

    def __init__(self, window, config):
        """Constructor."""
        self._window = window
        self._config = config
        self._documents = {}

        for document in self._window.get_documents():
            self._initialize_documenthelper(document)

        self._tab_add_handler = self._window.connect('tab-added',
                                                     self._on_tab_added)
        self._tab_remove_handler = self._window.connect('tab-removed',
                                                        self._on_tab_removed)

    def deactivate(self):
        """Deactivate plugin for this window."""
        for document in self._window.get_documents():
            self._deactivate_documenthelper(document)

        self._documents = None

        self._window.disconnect(self._tab_add_handler)
        self._window.disconnect(self._tab_remove_handler)

        self._config = None
        self._window = None

    def _on_tab_added(self, window, tab):
        """Callback on new tab added."""
        self._initialize_documenthelper(tab.get_document())

    def _on_tab_removed(self, window, tab):
        """Callback on tab removal - deactivates the DocumentHelper."""
        self._deactivate_documenthelper(tab.get_document())

    def _initialize_documenthelper(self, document):
        """Initializes a DocumentHelper for document if unknown as of now."""
        if (document and (not document in self._documents)):
            self._documents[document] = DocumentHelper(document, self._config)

    def _deactivate_documenthelper(self, document):
        """Deactivates a DocumentHelper for document if known."""
        if (document and (document in self._documents)):
            self._documents[document].deactivate()
            del self._documents[document]
