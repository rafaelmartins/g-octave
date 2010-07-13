Quick Start
===========

This is a svery small set of instructions for the users that just want
to install a package, and don't care about things like which package manager
g-octave will use or where g-octave will store your files.


Installing g-Octave
-------------------

With layman installed, install the science overlay::
    
    # layman -a science

Install g-octave::

    # emerge -av g-octave

Install g-octave's package database::

    # emerge --config g-octave


Installing the package
----------------------

If you don't care about configurations, the default values are good enough
for you, then just type::
    
    # g-octave -av packagename


Just a line!
------------

If you're really lazy, you can just type::

    # layman -a science && emerge g-octave && emerge --config g-octave && g-octave packagename

If all is ok, your package should be installed now!
