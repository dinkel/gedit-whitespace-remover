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

import gedit

from config_dialog import ConfigDialog
from config_settings import ConfigSettings
from window_helper import WindowHelper

class WhitespaceRemoverPlugin(gedit.Plugin):
    """Plugin that removes unnecessary whitespace."""

    def __init__(self):
        """Constructor."""
        gedit.Plugin.__init__(self)
        self._instances = {}
        self._config = ConfigSettings()

    def activate(self, window):
        """Activate the plugin for a window."""
        self._instances[window] = WindowHelper(window, self._config)

    def deactivate(self, window):
        """Deactivate the plugin for a window."""
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        """Simply returns - no user interface update is to be handled."""
        pass

    def is_configurable(self):
        """Returns that this plugin is configurable."""
        return True

    def create_configure_dialog(self):
        """Show the plugin settings window."""
        return ConfigDialog(self, self._config)
