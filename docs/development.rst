Development
===========

:Source code: http://git.overlays.gentoo.org/gitweb/?p=proj/g-octave.git
:Bugs to: rafael [at] rafaelmartins [dot] eng [dot] br

Running the test suites
-----------------------

You can run the tests suites using the script ``run_tests.py`` that can be
found in the directory ``scripts`` in the recent `source tarballs`_ or
in the `Git repository`_

.. _`source tarballs`: http://soc.dev.gentoo.org/~rafaelmartins/g-octave/
.. _`Git repository`: http://git.overlays.gentoo.org/gitweb/?p=proj/g-octave.git

::
    
    $ scripts/run_tests.py

If some test is broken, report me a bug by email. The bug tracker is
temporary disabled.


Creating source tarballs from the octave-forge SVN repository
-------------------------------------------------------------

We have a script to create source tarballs for all the packages,
using the latest stable revision from the octave-forge SVN repo.

To use it, add a ``pkg_cache`` option to your configuration file with
the directory where you want to save the generated tarballs and, after
clone the Mercurial repository or download the source tarball, run from
the root of the source tree::

    $ scripts/package_sources.py


Creating a package database from the previously created source tarballs
-----------------------------------------------------------------------

You should want to also create a package database. For this, keep the
``pkg_cache`` option in your configuration file pointing to the directory
with your source tarballs and run from the root of the source tree::

    $ scripts/package_database.py /path/to/your/new/database.tar.gz


Sending patches
---------------

You can send git formated patches to me via email.

More information will be available soon.
