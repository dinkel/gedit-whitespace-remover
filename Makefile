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

# Version of the program (to be updated when creating new packages)
VERSION=0.4.0

# Name of the program
APPLICATION=gedit-whitespace-remover

# Short name of the application
SHORT_NAME=whitespace_remover

# Local gedit plugin directoy
GEDIT_LOCAL_PLUGIN_DIR=~/.local/share/gedit/plugins

# GSchema directory
GSCHEMA_DIR=~/.local/share/glib-2.0/schemas

# GSchema name
GSCHEMA_NAME=org.gnome.gedit.plugins.whitespace-remover.gschema.xml

# Original author
AUTHOR="Christian Luginbühl"
AUTHOR_EMAIL="dinkel@pimprecords.com"

# Python executable
PYTHON=python3

# Name of the translations files (without extension)
DOMAIN=messages

# Dummy target, that intercepts the call to 'make' (without explicit target)
dummy:
	echo "Possible targets are: dist, tgz, zip, update-locales, create-locale LOCALE={ll[_CC]}, test, schematest, unittest, disttest, clean, mrproper, install, install-dev, uninstall\n"

# Tests and on success creates the packages
safe-dist: test dist

# Creates the .zip and .tar.gz packages
dist: tgz zip

# Packs everything needed to be deployed as a plugin into a gzipped tar
tgz: _create-distdir compile-locales
	tar czf dist/$(APPLICATION)-$(VERSION).tar.gz \
	        README.md \
	        $(SHORT_NAME).plugin \
	        $(SHORT_NAME)/ \
	        --exclude *.po \
	        --exclude *.pyc
	cd dist && \
	md5sum $(APPLICATION)-$(VERSION).tar.gz \
	       > $(APPLICATION)-$(VERSION).tar.gz.md5 && \
	gpg --detach-sign $(APPLICATION)-$(VERSION).tar.gz

# Packs everything needed to be deployed as a plugin into a zip
zip: _create-distdir compile-locales
	zip -qr dist/$(APPLICATION)-$(VERSION).zip \
	        README.md \
	        $(SHORT_NAME).plugin \
	        $(SHORT_NAME)/ \
	        -x *.po *.pyc
	cd dist && \
	md5sum $(APPLICATION)-$(VERSION).zip \
	       > $(APPLICATION)-$(VERSION).zip.md5 && \
	gpg --detach-sign $(APPLICATION)-$(VERSION).zip

# Creates a new locale provided in the LOCALE-variable with a new .po-file
create-locale: _generate-pot _create_localedir
	if [ -n "$(LOCALE)" ] ; then \
		if [ ! -e "$(SHORT_NAME)/locale/$(LOCALE)/LC_MESSAGES/$(DOMAIN).po" ] ; then \
			msginit --locale=$(LOCALE) \
				    --input=$(DOMAIN).pot \
				    --output="$(SHORT_NAME)/locale/$(LOCALE)/LC_MESSAGES/$(DOMAIN).po" ; \
		    sed -i 's/PACKAGE/$(APPLICATION)/g' $(SHORT_NAME)/locale/$(LOCALE)/LC_MESSAGES/$(DOMAIN).po ; \
			echo "Make sure to also update '$(SHORT_NAME).plugin'" ; \
		fi \
	else \
		echo "Usage is: make create-locale LOCALE={ll[_CC]}\n" ; \
	fi

# Merges all locales with a new generated .pot-template
update-locales: _generate-pot
	find $(SHORT_NAME)/locale/ \
	     -name $(DOMAIN).po \
	     -exec msgmerge --update \
	                    --backup=none \
	                    {} $(DOMAIN).pot \;

# Generates the binary l10n .mo-files for all known languages
compile-locales:
	find $(SHORT_NAME)/locale/*/LC_MESSAGES \
	     -type d \
	     -exec msgfmt {}/$(DOMAIN).po -o {}/$(DOMAIN).mo \;

# Runs all tests
test: schematest unittest disttest

# Runs the gschema test
schematest:
	glib-compile-schemas --dry-run --strict $(SHORT_NAME)

# Runs the unittests
unittest:
	$(PYTHON) ./test/unit/alltests.py

# Runs the disttests
disttest:
	$(PYTHON) ./test/dist/locale_in_pluginfile_test.py

# Cleans up the directory sturcture
clean:
	rm -rf dist/
	rm -f $(DOMAIN).pot

# Cleans more thoroughly (including .mo-files and .pyc that are not needed for git updates)
mrproper: clean
	find . -name "*.pyc" -exec rm {} \;
	rmdir `find . -name "__pycache__"`
	find $(SHORT_NAME)/locale -name "*.mo" -exec rm {} \;

# Installs the plugin locally
install: safe-dist uninstall
	mkdir -p $(GEDIT_LOCAL_PLUGIN_DIR) $(GSCHEMA_DIR)
	tar zxfv dist/$(APPLICATION)-$(VERSION).tar.gz -C $(GEDIT_LOCAL_PLUGIN_DIR)
	rm $(GEDIT_LOCAL_PLUGIN_DIR)/README
	mv $(GEDIT_LOCAL_PLUGIN_DIR)/$(SHORT_NAME)/$(GSCHEMA_NAME) $(GSCHEMA_DIR)
	glib-compile-schemas $(GSCHEMA_DIR)

# Symlinks the development version of the plugin locally
install-dev: uninstall
	mkdir -p $(GEDIT_LOCAL_PLUGIN_DIR) $(GSCHEMA_DIR)
	ln -s `pwd`/$(SHORT_NAME).plugin \
	      `pwd`/$(SHORT_NAME)/ \
	      $(GEDIT_LOCAL_PLUGIN_DIR)
	ln -s $(GEDIT_LOCAL_PLUGIN_DIR)/$(SHORT_NAME)/$(GSCHEMA_NAME) $(GSCHEMA_DIR)
	glib-compile-schemas $(GSCHEMA_DIR)

uninstall:
	rm -rf $(GEDIT_LOCAL_PLUGIN_DIR)/$(SHORT_NAME)*
	rm -f $(GSCHEMA_DIR)/$(GSCHEMA_NAME)
	glib-compile-schemas $(GSCHEMA_DIR)

# Creates a dist/ directory where packages are saved (private)
_create-distdir:
	mkdir -p dist

# Creates a directory structure for a new locale if set (private)
_create_localedir:
	if [ -n "$(LOCALE)" ] ; then \
		mkdir -p $(SHORT_NAME)/locale/$(LOCALE)/LC_MESSAGES ; \
	fi

# Generates a l10n .po-template by searching through source files (private)
_generate-pot:
	xgettext --language=Python \
	         --copyright-holder=$(AUTHOR) \
	         --package-name=$(APPLICATION) \
	         --package-version=$(VERSION) \
	         --msgid-bugs-address=$(AUTHOR_EMAIL) \
	         --output=$(DOMAIN).pot \
	         $(SHORT_NAME)/*.py
