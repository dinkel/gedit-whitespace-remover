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

class DocumentManipulator(object):
    """Provides class methods that manipluate a GtkTextBuffer object."""

    @classmethod
    def strip_trailing_blank_lines(_cls_, doc, preserve_cursor):
        """Delete trailing newlines at the end of the document."""
        cursor_line = doc.get_iter_at_mark(doc.get_insert()).get_line()
        buffer_end = doc.get_end_iter()

        if buffer_end.starts_line():
            itr = buffer_end.copy()
            while itr.backward_line():
                if (preserve_cursor and
                    itr.get_line() < cursor_line):
                    itr.forward_line()
                    break
                if not itr.ends_line():
                    itr.forward_to_line_end()
                    break
            doc.delete(itr, buffer_end)

    @classmethod
    def strip_trailing_spaces_on_lines(_cls_, doc, preserve_cursor):
        """Delete trailing space at the end of each line."""
        cursor_line = doc.get_iter_at_mark(doc.get_insert()).get_line()
        buffer_end = doc.get_end_iter()

        for line in range(buffer_end.get_line() + 1):
            line_end = doc.get_iter_at_line(line)
            if not line_end.ends_line():
                line_end.forward_to_line_end()
            itr = line_end.copy()
            while itr.backward_char():
                if (preserve_cursor and
                    line == cursor_line and
                    (itr.compare(doc.get_iter_at_mark(doc.get_insert())) < 0)):
                    itr.forward_char()
                    break
                if not itr.get_char() in (" ", "\t"):
                    itr.forward_char()
                    break
            doc.delete(itr, line_end)
