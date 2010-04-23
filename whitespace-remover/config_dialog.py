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

import gtk

from localization import Localization

class ConfigDialog(gtk.Dialog):
    """Configuration dialog."""

    def __init__(self, plugin, config = None):
        """Constructor."""
        self._config = config

        Localization.setup()

        gtk.Dialog.__init__(self,
                            _("Settings"),
                            None,
                            gtk.DIALOG_DESTROY_WITH_PARENT)

        self.set_resizable(False)

        close_button = self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        close_button.grab_default()
        close_button.connect_object("clicked", gtk.Widget.destroy, self)

        main_box = gtk.VBox(False, 0)
        main_box.set_border_width(12)

        title_label = gtk.Label()
        title_label.set_markup(
            '<b>' + _("Actions to perform upon saving:") + '</b>')
        title_label.set_alignment(0, 0)

        config_box = gtk.VBox(False, 6)
        config_box.set_border_width(6)

        checkbox_label = _("_Strip trailing whitespace on every line")
        whitespace_checkbox = gtk.CheckButton(checkbox_label)
        whitespace_checkbox.connect('clicked',
                                    self.update_setting,
                                    'remove_whitespace')
        whitespace_checkbox.set_active(
            self._config.get_bool('remove_whitespace'))

        checkbox_label = _("_Remove newlines at the end of document")
        newlines_checkbox = gtk.CheckButton(checkbox_label)
        newlines_checkbox.connect('clicked',
                                  self.update_setting,
                                  'remove_newlines')
        newlines_checkbox.set_active(self._config.get_bool('remove_newlines'))

        config_box.pack_start(whitespace_checkbox, True, True, 0)
        config_box.pack_start(newlines_checkbox, True, True, 0)

        main_box.pack_start(title_label, True, True, 0)
        main_box.pack_start(config_box, True, True, 0)

        self.vbox.pack_start(main_box, True, True, 0)

        self.show_all()

    def update_setting(self, widget, data = None):
        """Updates the boolean gconf value passed as parameter."""
        self._config.set_bool(data, widget.get_active())
