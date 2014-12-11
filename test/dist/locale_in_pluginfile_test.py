#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Whitespace Remover - gedit plugin
# Copyright (C) 2010-2014  Christian Luginbühl
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

import os
import sys
import glob
import time

errors = []

count = 0

# Helper "constants"
PLUGIN_FILE = 'whitespace_remover.plugin'

MISSING_NAME = "Missing 'Name[]' localization in " + PLUGIN_FILE + \
               " for locale "

MISSING_DESC = "Missing 'Description[]' localization in " + PLUGIN_FILE + \
               " for locale "

ROOT_PATH = os.path.join(os.path.dirname(__file__), '..', '..')

# Helper methods
def _get_all_po_paths(root_path):
    return glob.glob(os.path.join(root_path,
                                  'whitespace_remover',
                                  'locale',
                                  '*',
                                  'LC_MESSAGES',
                                  '*.po'))

def _get_locale(path):
    return os.path.basename(os.path.dirname(os.path.dirname(path)))

def _get_file_contents(path):
    contents = ''
    fh = open(path, 'r')
    contents = fh.read()
    fh.close()

    return contents

def _check_localizations_in_string(all_po_paths, contents):
    global count

    for po_path in all_po_paths:
        locale = _get_locale(po_path)

        if (plugin_file_contents.find('Name[' + locale + ']=') != -1):
            sys.stdout.write('.')
        else:
            errors.append(MISSING_NAME + "'" + locale + "'")
            sys.stdout.write('E')

        if (plugin_file_contents.find('Description[' + locale + ']=') != -1):
            sys.stdout.write('.')
        else:
            errors.append(MISSING_DESC + "'" + locale + "'")
            sys.stdout.write('E')

        count = count + 2

# Start of program

starttime = time.clock()

all_po_paths = _get_all_po_paths(ROOT_PATH)

plugin_file_contents = _get_file_contents(os.path.join(ROOT_PATH, PLUGIN_FILE))

_check_localizations_in_string(all_po_paths, plugin_file_contents)

print('')
print('----------------------------------------------------------------------')

time = time.clock() - starttime

print('Ran %s locale consistency checks in %0.3fs' % (count, time))
print('')


if (not errors):
    print('OK')
else:
    for error in errors:
        print('ERROR: ' + error)
    exit(1)
