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

import gconf

class ConfigSettings():
    """Handles the configuration setting in gconf."""

    _gconf_base = "/apps/gedit-2/plugins/whitespace-remover/"

    _default_remove_whitespace = True
    _default_remove_newlines = True

    def __init__(self):
        """Constructor."""
        if not self._has_key('remove_whitespace'):
            self._set_bool_forced('remove_whitespace',
                                  self.__class__._default_remove_whitespace)


        if not self._has_key('remove_newlines'):
            self._set_bool_forced('remove_newlines',
                                  self.__class__._default_remove_newlines)

    def _has_key(self, key):
        """Test if a key exists."""
        key = self.__class__._gconf_base + key
        return (gconf.client_get_default().get(key) is not None)

    def get_bool(self, key):
        """Retrieve a gconf key."""
        if not self._has_key(key):
            raise Exception('unknown gconf key')

        key = self.__class__._gconf_base + key
        return gconf.client_get_default().get_bool(key)

    def set_bool(self, key, true_or_false):
        """Save a value to a gconf key."""
        if not self._has_key(key):
            raise Exception('unknown gconf key')

        self._set_bool_forced(key, true_or_false)

    def _set_bool_forced(self, key, true_or_false):
        """Saves a value to a gconf key without checking its existance."""
        key = self.__class__._gconf_base + key
        value = gconf.Value(gconf.VALUE_BOOL)
        value.set_bool(true_or_false)
        gconf.client_get_default().set(key, value)
