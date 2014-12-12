Whitespace Remover - gedit plugin
=================================

This plugin for gedit - GNOME text editor - aims to provide a few (actually only two) additional convenience methods. Upon saving it will remove whitespace from the end of all lines and remove trailing newlines from the end of the document.

This plugin was heavily inspired and is in parts based on Osmo Salomaa's trailsave plugin <http://users.tkk.fi/~otsaloma/gedit/>. Out of a supposed missing feature (that proved to be inside of gedit already - thanks for pointing this out Osmo) and of having a nice sandbox to learn Python, this plugin was brought to life. It extends its predecessor by the ability to configure its actions on the UI, i18n support and unittests (you might want to call this bloat ;-)).

Contact
-------

Author: Christian Luginbühl <dinkel@pimprecords.com>

Home: <http://github.com/dinkel/gedit-whitespace-remover/>

License
-------

See the `LICENSE` file.

Install
-------

Simply extract the package into the `~/.local/share/gedit/plugins` directory, or - for a system-wide deployment - into `/usr/lib/gedit/plugins` (the path may be different, depending on your distribution).

A little more tricky is the installation of the new GSettings schema file, that provides the permanent configuration.

If you are having root access:

Copy or move the file `org.gnome.gedit.plugin.whitespace-remover.gschema.xml` into `/usr/share/glib-2.0/schemas/` and run

    $ sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

If you do *not* have root access:

Copy or move the file `org.gnome.gedit.plugin.whitespace-remover.gschema.xml` into `~/.local/share/glib-2.0/schemas/` (you might need to create this  directory first). Run:

    $ glib-compile-schemas ~/.local/share/glib-2.0/schemas/

Additionally you need to make sure that `~/.local/share` is in the environment variable `XDG_DATA_DIRS` (this is due to an im my opinion wrong behaviour of GSettings and described in [https://bugzilla.gnome.org/show_bug.cgi?id=741335]).

The to me nicest way to do is to add the following lines to `~/.profile` (or similar):

    export XDG_DATA_HOME=$HOME/.local/share
    export XDG_DATA_DIRS=$XDG_DATA_HOME:$XDG_DATA_DIRS

Finally:

Then activate and configure the plugin through Edit -> Preferences -> Plugins.

Development
-----------

The Makefile provided has quite a few nice methods for package generation, testing and especially for adding new languages. Even though everybody can read the Makefile for finding about the possible targets, here are a few short notices for adding/updating new languages:

Creating a new locale:

    $ make create-locale LOCALE=it_IT (or simply LOCALE=it)

Updating all .po-files (creating and merging a new .pot-template):

    $ make update-locales

Compiling locales (creating new .mo-files):

    $ make compile-locales

It proved helpful for development to check out the git-repository to your favourite location and create symlinks in your personal plugins directory to the necessary files and directories. There is a make target, that accomplishes this:

    $ make install-dev

Note that you also need to deal with the GSettings schema as described above in the non-root section.

In order tu run tests, one needs to symlink the Gedit-3.0.typelib file into /usr/lib/girepository-1.0, so that "from gi.repository import Gedit" works (e.g. needed when running unit tests). In Ubuntu do:

    $ sudo ln -s /usr/lib/x86_64-linux-gnu/gedit/girepository-1.0/Gedit-3.0.typelib /usr/lib/girepository-1.0

Comments / Bugs
---------------

Although I do consider myself as a skilled programmer, these are my first steps in Python and gedit plugin programming. Therefore I'm eager to hear your comments about this piece of software. Also if you find a bug or thought of an enhancement, please use GitHubs bugtracking system. This plugin's home is stated above.
