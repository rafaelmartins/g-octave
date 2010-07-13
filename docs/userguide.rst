User Guide
==========

This is a small user guide for g-Octave, with some instructions to the
end user.


Installing g-Octave
-------------------

The ebuilds for g-Octave will be available on the Portage tree as soon
as possible. For now, they can be found on the Gentoo ``science`` overlay.
To install it with ``layman`` and ``git`` installed, type::

    # layman -a science


After you have the overlay installed, you can install the package, using: ::
    
    # emerge -av app-portage/g-octave

We have 2 ebuilds, one for the latest stable release (for ``~x86`` and ``~amd64``)
and one live ebuild, that installs g-Octave from the mercurial repository
(without keywords). If you want to use the live ebuild, you need to unmask
this ebuild, adding the line below to ``/etc/portage/package.keywords``::

    app-portage/g-octave **

The live ebuild is only recommended for who want to help testing new
features, or for developers.

Stable users (with ``x86`` or ``amd64``) that wants to test the latest
release will need to unmask the ebuild too, adding this to
/etc/portage/package.keywords (e.g. for ``x86``)::

    app-portage/g-octave ~x86

The source code of g-Octave can be found in this Git repository:

http://git.overlays.gentoo.org/gitweb/?p=proj/g-octave.git;a=summary

You can clone the Git repository using this command (with Git
installed, of course)::
    
    $ git clone git://git.overlays.gentoo.org/proj/g-octave.git

The release tarballs can be found here:

http://soc.dev.gentoo.org/~rafaelmartins/g-octave/releases/


Configuring g-Octave
--------------------

Using the file ``/etc/g-octave.cfg``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you installed g-Octave correctly, you should find a configuration file
at ``/etc/g-octave.cfg``.

The main options are ``package_manager``, ``db`` and ``overlay``, that
defines the package manager used by g-octave and the directory paths
for the package database and the generated overlay, respectively.

Other options are available. Please read the comments in the configuration
file.


Using environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~






Syncronizing the package database
---------------------------------

Currently g-Octave depends on an external package database, in order to
create the ebuilds for the packages. You'll need to fetch this database
in the first time that you run g-Octave: ::
    
    # g-octave --sync


Configuring your package manager
--------------------------------

g-octave can use all the 3 package managers available to Gentoo Linux:
Portage, Paludis and Pkgcore.

You just need to setup the option ``package_manager`` in the config file
with the lowercase name of the package manager: portage, paludis, pkgcore.

If you're using Paludis or Pkgcore, you'll need to configure the overlay
in your package manager configuration files. Please check the documentation
of your package manager:

- Paludis: http;//paludis.pioto.org/
- Pkgcore: http://www.pkgcore.org/

Portage will works out of the box.


Installing packages
-------------------

You can list all the available packages using this command: ::
    
    # g-octave --list

or ::
    
    # g-octave -l

To install a package, use: ::
    
    # g-octave packagename

or ::
    
    # g-octave packagename-version

For example: ::
    
    # g-octave control-1.0.11

``g-octave`` command-line tool supports some options for the installation
of packages:
    
``-a`` or ``--ask``
    Ask before install the package
``-p`` or ``--pretend``
    Only pretend the installation of the package

You can get some information about the package using this command: ::

    # g-octave --info packagename

or ::
    
    # g-octave -i packagename


Installing packages from the octave-forge SVN repository
--------------------------------------------------------

If you want to test some new feature, or to use the new version of the
packages ever, you'll like to install your packages directly from the
SVN repository.

To install a package from SVN, type::
    
    # g-octave packagename-9999

All the common g-octave options for install packages are allowed, and
the special version ``9999`` says to g-octave that you want to use the
SVN version.

In order to be able to install packages from svn you need to install
g-octave with the USE flag ``svn`` enabled.


Uninstalling packages
---------------------

You can uninstall packages using this command: ::

    # g-octave --unmerge packagename

or ::
    
    # g-octave -C packagename-version

The options ``--ask`` and ``--verbose`` are also supported.
