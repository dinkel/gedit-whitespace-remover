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

import unittest
import sys
import os

import gconf

sys.path.append(os.path.join(os.path.dirname(__file__),
                             '..',
                             '..',
                             'whitespace-remover'))

from config_settings import ConfigSettings

class ConfigSettingsTest(unittest.TestCase):

    _gconf_base = '/apps/gedit-2/plugins/whitespace-remover/'

    def setUp(self):
        self._config = ConfigSettings()

    def test_return_type(self):
        self.assertTrue(isinstance(self._config.get_bool('remove_whitespace'),
                                   bool))

    def test_write_read_with_true(self):
        self._config.set_bool('remove_whitespace', True)
        self.assertTrue(self._config.get_bool('remove_whitespace'))

    def test_write_read_with_false(self):
        self._config.set_bool('remove_whitespace', False)
        self.assertFalse(self._config.get_bool('remove_whitespace'))

    def test_reading_unknown_key_fails(self):
        self.assertRaises(Exception, self._config.get_bool, 'unknown')

    def test_writing_unknown_key_fails(self):
        self.assertRaises(Exception, self._config.set_bool, 'unknown', True)

    def test_intializing_writes_defaults(self):
        key = self.__class__._gconf_base + 'remove_whitespace'
        gconf.client_get_default().unset(key)
        self.assertRaises(Exception,
                          self._config.get_bool, 'remove_whitespace')
        config = ConfigSettings()
        self.assertTrue(config.get_bool('remove_whitespace'))


if __name__ == '__main__':
    unittest.main()
