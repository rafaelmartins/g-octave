Development
===========

:Source code: http://git.overlays.gentoo.org/gitweb/?p=proj/g-octave.git
:Bugs to: http://www.g-octave.org/trac/newticket

.. warning::
    
    This section of the documentation is supposed to be used by g-Octave
    developers. End-users should not need to read this!


Running the test suites
-----------------------

You can run the tests suites using the script ``run_tests.py`` that can be
found in the directory ``scripts`` in the recent `source tarballs`_ or
in the `Git repository`_

.. _`source tarballs`: http://www.g-octave.org/releases/
.. _`Git repository`: http://git.overlays.gentoo.org/gitweb/?p=proj/g-octave.git

::
    
    $ scripts/run_tests.py


If some test is broken, please use the `bug tracker`_.

.. _`bug tracker`: http://www.g-octave.org/trac/newticket


Working on the package database
-------------------------------

Package databases are Git repositories with the DESCRIPTION files, patches
and a ``info.json`` file with the non-octave dependencies and the licenses
of the packages.

We're using github to host the package database:

http://github.com/rafaelmartins/g-octave-db/

If you want to fix something on the package database, please fork the
repository, change it and fill a merge request.


Updating the package database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have a script to update the package database: ``contrib/manage_pkgdb.py``.
You just need to clone the git repository and create a directory to store
the source tarballs, that are used to extract the DESCRIPTION files and
build the package database.

g-Octave will install the script on ``/usr/share/g-octave/contrib``

::

    $ git clone git+ssh://git@github.com:your_username/g-octave-db.git
    $ mkdir tarballs
    $ /usr/share/g-octave/contrib/manage_pkgdb.py tarballs g-octave-db

The first parameter of the script is the path to the directory that will
store the tarballs. The second parameter is the path to the local clone
of your forked git repository.


Updating the list of external dependencies and licenses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have a script to update the JSON file that contains the external
dependencies (non-octave packages from the portage tree) and the licenses
(the license names used by the octave-forge developers doesn't matches
with the names used on the Portage tree).

This script will be also installed on ``/usr/share/g-octave/contrib``

::
    
    $ /usr/share/g-octave/contrib/manage_info.py g-octave-db/info.json

The script is interactive and the argument is the path to the ``info.json``
file, that lives on the root of the Git repository of the package database.

The script will suggest some matches for each dependency. For the licenses
you need to find the best match at the directory ``${PORTDIR}/licenses``,
where ${PORTDIR} is the path to your Portage tree (``/usr/portage``
usually).


Commiting the changes
~~~~~~~~~~~~~~~~~~~~~

You can use the script ``manage_pkgdb.py`` to commit the changes::

    $ /usr/share/g-octave/contrib/manage_pkgdb.py --commit tarballs g-octave-db

The script will do a last check on your updates and commit the stuff to
your fork repository.


Using your fork as package database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use your fork as package database, change the variable
``db_mirror`` on the file ``/etc/g-octave.cfg`` to something like::
    
    db_mirror = github://your_username/g-octave-db


Sending patches to the source code
----------------------------------

The source code of g-Octave lives on a repository on the Gentoo Linux
infrastructure. ::

    $ git clone git://git.overlays.gentoo.org/proj/g-octave.git

You can change what you need, commit, generate a Git-formated patch and
attach it to a new ticket on our `bug tracker`_.
