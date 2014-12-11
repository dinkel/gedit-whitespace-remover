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

from gi.repository import Gio

class ConfigSettings():
    """Handles the configuration settings."""

    SCHEMA_ID = "org.gnome.gedit.plugins.whitespace-remover"

    def __init__(self):
        """Constructor."""
        self._settings = Gio.Settings.new(self.SCHEMA_ID)

    def _assert_key(self, key):
        """Assert that a key exists, otherwise throw an exception."""
        if key not in self._settings.list_keys():
            raise Exception('unknown gsettings key')

    def get_bool(self, key):
        """Retrieve the boolean value for key."""
        self._assert_key(key);

        return self._settings.get_boolean(key);

    def set_bool(self, key, true_or_false):
        """Save a boolean value for a given key."""
        self._assert_key(key);

        self._settings.set_boolean(key, true_or_false);
