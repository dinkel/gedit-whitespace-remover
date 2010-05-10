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

from document_manipulator import DocumentManipulator

class DocumentHelper:
    """Handles a document instance and reacts on saving events."""

    def __init__(self, document, config):
        self._document = document
        self._config = config

        self._saving_handler = self._document.connect('saving',
                                                      self._on_saving)

    def deactivate(self):
        """Disconnects the saving-event."""
        self._document.disconnect(self._saving_handler)

        self._config = None
        self._document = None

    def _on_saving(self, doc, *args):
        """Strip trailing spaces in document."""

        doc.begin_user_action()
        if (self._config.get_bool('remove_whitespace')):
            DocumentManipulator.strip_trailing_spaces_on_lines(doc)

        if (self._config.get_bool('remove_newlines')):
            DocumentManipulator.strip_trailing_blank_lines(doc)

        doc.end_user_action()
