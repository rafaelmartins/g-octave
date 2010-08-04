Upgrading g-Octave
==================

Quick notes for users upgrading from older versions of g-Octave.


From ``0.3`` to ``0.4``
-----------------------

This version broke the compatibility with old package databases and some
external files.

You'll need to remove the directories of the package database and the
overlay (``db`` and ``overlay`` options from the configuration file).

To know what are the current values, type::
    
    $ g-octave --config db
    $ g-octave --config overlay

And remove both directories before run ``emerge --config =g-octave-0.4``
