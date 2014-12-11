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

from gi.repository import Gtk

sys.path.append(os.path.join(os.path.dirname(__file__),
                             '..',
                             '..',
                             'whitespace_remover'))

from document_manipulator import DocumentManipulator

class DocumentManipulatorTest(unittest.TestCase):

    def setUp(self):
        self.raw_unix = self._get_textbuffer('unix_utf8_raw.txt')

    def test_unix_utf8_strip_whitespace(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_whitespace.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix,
                                                           False)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_whitespace_multiple(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_whitespace.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix,
                                                           False)
        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix,
                                                           False)
        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix,
                                                           False)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_newlines(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_newlines.txt')

        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix,
                                                       False)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_newlines_multiple(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_newlines.txt')

        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix,
                                                       False)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix,
                                                       False)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix,
                                                       False)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_whitespace_then_newlines(self):
        resulting = self._get_textbuffer(
            'unix_utf8_stripped_whitespace_then_newlines.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix,
                                                           False)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix,
                                                       False)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_stripping_not_symmetrical(self):
        """NOTE: This is neither good nor bad, the test just shows it."""
        other_way = self._get_textbuffer('unix_utf8_raw.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix,
                                                           False)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix,
                                                       False)

        DocumentManipulator.strip_trailing_blank_lines(other_way,
                                                       False)
        DocumentManipulator.strip_trailing_spaces_on_lines(other_way,
                                                           False)

        self.assertNotEqual(self._get_contents(self.raw_unix),
                            self._get_contents(other_way))

    def test_win_utf8_strip_whitespace_then_newlines(self):
        raw_win = self._get_textbuffer('win_utf8_raw.txt')

        resulting = self._get_textbuffer(
            'win_utf8_stripped_whitespace_then_newlines.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(raw_win,
                                                           False)
        DocumentManipulator.strip_trailing_blank_lines(raw_win,
                                                       False)

        self.assertEqualContents(resulting, raw_win)

    def test_different_line_endings(self):
        raw_different = self._get_textbuffer('different_utf8_raw.txt')

        resulting = self._get_textbuffer(
            'different_utf8_stripped_newlines.txt')

        DocumentManipulator.strip_trailing_blank_lines(raw_different,
                                                       False)

        self.assertEqualContents(resulting, raw_different)

    def test_preserve_cursor(self):
        resulting = self._get_textbuffer(
            'unix_utf8_stripped_whitespace_then_newlines_cursor_near_end.txt')

        near_end = self.raw_unix.get_iter_at_line_offset(9, 1)

        self.raw_unix.place_cursor(near_end)

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix,
                                                           True)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix,
                                                       True)

        self.assertEqualContents(resulting, self.raw_unix)


    def assertEqualContents(self, expected, actual):
        self.assertEqual(self._get_contents(expected),
                         self._get_contents(actual))

    def _get_textbuffer(self, filename):
        buffer = Gtk.TextBuffer()

        f = open(os.path.join(os.path.dirname(__file__), filename), 'r')
        buffer.set_text(f.read())
        f.close()

        return buffer

    def _get_contents(self, buffer):
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()

        return buffer.get_text(start, end, True)



if __name__ == '__main__':
    unittest.main()
