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

sys.path.append(os.path.join(os.path.dirname(__file__),
                             '..',
                             '..',
                             'whitespace_remover'))

from localization import Localization

class LocalizationTest(unittest.TestCase):

    def test_not_dying_when_calling(self):
        try:
            Localization.setup()
        except:
            self.fail('Localization.setup did raise an error')


if __name__ == '__main__':
    unittest.main()
