Development
===========

:Source code: http://g-octave.rafaelmartins.eng.br/hg/
:Bug tracker: http://g-octave.rafaelmartins.eng.br/

.. _`bug tracker`: http://g-octave.rafaelmartins.eng.br/

Running the test suites
-----------------------

You can run the tests suites using the script ``run_tests.py`` that can be
found in the directory ``scripts`` in the `source tarballs`_ (since 0.1) or
in the `Mercurial repository`_

.. _`source tarballs`: http://g-octave.rafaelmartins.eng.br/distfiles/releases/
.. _`Mercurial repository`: http://g-octave.rafaelmartins.eng.br/hg/

::
    
    $ scripts/run_tests.py

If some test is broken, please create a ticket in the `bug tracker`_.
A quick registration is needed.


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

You can send mercurial/git formated patches, attaching the patch to a new
bug in the `bug tracker`_.

More information will be available soon.
