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
import gtk

sys.path.append(os.path.join(os.path.dirname(__file__),
                             '..',
                             '..',
                             'whitespace-remover'))

from document_manipulator import DocumentManipulator

class DocumentManipulatorTest(unittest.TestCase):

    def setUp(self):
        self.raw_unix = self._get_textbuffer('unix_utf8_raw.txt')

    def test_unix_utf8_strip_whitespace(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_whitespace.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_whitespace_multiple(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_whitespace.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix)
        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix)
        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_newlines(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_newlines.txt')

        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_newlines_multiple(self):
        resulting = self._get_textbuffer('unix_utf8_stripped_newlines.txt')

        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_unix_utf8_strip_whitespace_then_newlines(self):
        resulting = self._get_textbuffer(
            'unix_utf8_stripped_whitespace_then_newlines.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix)

        self.assertEqualContents(resulting, self.raw_unix)

    def test_stripping_not_symmetrical(self):
        """NOTE: This is neither good nor bad, the test just shows it."""
        other_way = self._get_textbuffer('unix_utf8_raw.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(self.raw_unix)
        DocumentManipulator.strip_trailing_blank_lines(self.raw_unix)

        DocumentManipulator.strip_trailing_blank_lines(other_way)
        DocumentManipulator.strip_trailing_spaces_on_lines(other_way)

        self.assertNotEqual(self._get_contents(self.raw_unix),
                            self._get_contents(other_way))

    def test_win_utf8_strip_whitespace_then_newlines(self):
        raw_win = self._get_textbuffer('win_utf8_raw.txt')

        resulting = self._get_textbuffer(
            'win_utf8_stripped_whitespace_then_newlines.txt')

        DocumentManipulator.strip_trailing_spaces_on_lines(raw_win)
        DocumentManipulator.strip_trailing_blank_lines(raw_win)

        self.assertEqualContents(resulting, raw_win)

    def text_different_line_endings(self):
        raw_random = self._get_textbuffer('different_utf8_raw.txt')

        resulting = self._get_textbuffer(
            'different_utf8_stripped_newlines.txt')

        DocumentManipulator.strip_trailing_blank_lines(raw_different)

        self.assertEqualContents(resulting, raw_different)


    def assertEqualContents(self, expected, actual):
        self.assertEqual(self._get_contents(expected),
                         self._get_contents(actual))

    def _get_textbuffer(self, filename):
        buffer = gtk.TextBuffer()

        f = open(os.path.join(os.path.dirname(__file__), filename), 'r')
        buffer.set_text(f.read())
        f.close()

        return buffer

    def _get_contents(self, buffer):
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()

        return buffer.get_text(start, end)



if __name__ == '__main__':
    unittest.main()
