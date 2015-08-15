User Guide
==========

This is an user guide with some instructions to the end-user.


Installing g-Octave
-------------------

The ebuilds for g-Octave are available on the Portage tree. You can install
the package, using::

    # emerge -av app-portage/g-octave

We have 2 ebuilds, one for with latest stable release (for ``~x86`` and
``~amd64``) and one live ebuild, that installs g-Octave from the Git
repository (without keywords). If you want to use the live ebuild, you
need to unmask it adding the line below to your
``/etc/portage/package.keywords``::

    app-portage/g-octave **

The live ebuild is only recommended for who want to help testing new
features, or for developers.

Stable users (with ``x86`` or ``amd64``) that wants to test the latest
release will need to unmask the ebuild too, adding this to
/etc/portage/package.keywords (e.g. for ``x86``)::

    app-portage/g-octave ~x86

The source code of g-Octave can be found in this Git repository:

https://github.com/rafaelmartins/g-octave/downloads

You can clone the Git repository using this command (with Git
installed, of course)::

    $ git clone git://github.com/rafaelmartins/g-octave.git

The release tarballs can be found here:

https://github.com/rafaelmartins/g-octave/downloads


USE flags
~~~~~~~~~

- ``doc``: Install this documentation. Depends on ``dev-python/sphinx``.


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

All the options from the configuration file can be overrided with environment
variables. The environment variable name starts with ``GOCTAVE_`` and
ends with the option name in uppercase. for example, ``GOCTAVE_OVERLAY``
will override the option ``overlay`` from the config file.

Usage example::

    # GOCTAVE_OVERLAY=/tmp/overlay g-octave -av packagename


Enabling the logging feature
----------------------------

If you want to write some relevant stuff to a log file you can enable
the logging feature, configuring the option ``log_level`` on the configuration.

The available options are: ``debug``, ``info``, ``warning``, ``error``, ``critical``.

You can change the location of the log file, using the option ``log_file``.
The default is: ``/var/log/g-octave.log``

Make sure that the user running g-octave have write permissions to ``log_file``.


Syncronizing the package database
---------------------------------

Currently g-Octave depends on an external package database, in order to
create the ebuilds for the packages. If you installed the live version of
g-Octave (=g-octave-9999) you'll need to fetch this database in the first
time that you run g-Octave (and whenever you want to updates): ::

    # g-octave --sync


Configuring your package manager
--------------------------------

g-octave can use all the 3 package managers available on Gentoo Linux:
**Portage**, **Paludis** and **Pkgcore**.

You just need to setup the option ``package_manager`` with the lowercase
name of the package manager: ``portage``, ``paludis``, ``pkgcore``.

If you're using **Paludis** or **Pkgcore**, you'll need to configure the overlay
in your package manager configuration files. Please check the documentation
of your package manager:

- Paludis: http://paludis.pioto.org/
- Pkgcore: http://www.pkgcore.org/

**Portage** works out of the box.


Installing packages
-------------------

From the upstream source tarballs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
``-1`` or ``--oneshot``
    Do not add the packages to the world file for later updating.


You can get some information about the package using this command: ::

    # g-octave --info packagename

or ::

    # g-octave -i packagename


From the octave-forge Mercurial repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to test some new feature or to always use the newest version
of the packages, you'll like to install the packages directly from the
Mercurial repository.

To install a package from Mercurial, you'll need to configure g-Octave, changing
the value of the variable ``use_scm`` on the file ``/etc/g-octave.cfg``
to ``true``. After that, type::

    # g-octave packagename

If you only want to install a single package, you can use the command-line
option ``--scm``.

If you enabled the installation from Mercurial on the configuration file and
wants to install a stable version, you can use the command-line option
``--no-scm``.


Updating packages
-----------------

You can update a package using this command: ::

    # g-octave --update packagename

or ::

    # g-octave -u packagename

If you want to update all the installed packages, run this without arguments::

    # g-octave --update

or ::

    # g-octave -u

The options ``--ask`` and ``--verbose`` are also supported.


Searching packages
------------------

You can do searches on the package names if you use the option ``-s`` or
``--search``. Regular expressions are allowed. ::

    # g-octave --search anything

or ::

    # g-octave -s ^con


Uninstalling packages
---------------------

You can uninstall packages using this command: ::

    # g-octave --unmerge packagename

or ::

    # g-octave -C packagename-version

The options ``--ask`` and ``--verbose`` are also supported.


Troubleshooting
---------------

Some times the generated ebuilds can be broken for some reason. To fix
this you can use the command-line option ``--force``, that will rebuild
the ebuild or the command-line option ``--force-all``, that rebuild the
entire overlay.

If you got some problem with corrupted sources, please remove the tarball
from the ``${DISTDIR}`` and run::

    # g-octave --force packagename

If you still have problems, please fill a ticket on our `bug tracker`_

.. _`bug tracker`: https://github.com/rafaelmartins/g-octave/issues
