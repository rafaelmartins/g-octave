Tinderbox
=========

g-Octave provides a script to run build tests for all the octave-forge
packages automatically and report issues to the `bug tracker`_.

.. _`bug tracker`: http://www.g-octave.org/trac/report/9

.. warning::

    This script is not intended to be used by end-users, only developers.


Creating the environment
------------------------

We recommend the use of the script inside a chroot environment. For this
you'll need to download the latest stage3 tarball from the Gentoo mirrors
and create a basic environment::
    
    # cd /home/user/g-octave
    # tar xvjpf stage3-*.tar.bz2


Configuring the environment
---------------------------

You should copy the needed files from your Gentoo installation to the
chroot environment, to ease the configuration. ::

    # cp /etc/resolv.conf /home/user/g-octave/etc
    # cp /etc/make.conf /home/user/g-octave/etc

You may also need some files from ``/etc/portage``


Mounting filesystems/directories
--------------------------------

You should mount your current ``${PORTDIR}`` (e.g. ``/usr/portage``)
inside the chroot dir (the script will force the use of Portage to build
the packages)::

    # mkdir /home/user/g-octave/usr/portage
    # mount -o bind /usr/portage /home/user/g-octave/usr/portage

Mounting ``/proc`` and ``/dev``::

    # mount -t proc none /home/user/g-octave/proc
    # mount -o bind /dev /home/user/g-octave/dev


Entering the chroot environment
-------------------------------

::

    # chroot /home/user/g-octave /bin/bash
    # env-update
    # source /etc/profile
    # export PS1="(g-octave) $PS1"


Updating the packages and installing the dependencies
-----------------------------------------------------

::

    # emerge -avuDN system
    # USE="git" emerge -av layman
    # layman -a science
    # FEATURES="test" USE="sync" emerge -av g-octave


Configuring g-Octave
--------------------

You should `create an account`_ on the `g-Octave project page`_, edit the
file ``/etc/g-octave.cfg`` and append the lines below (with your data)::

    trac_user = username
    trac_passwd = password

.. _`create an account`: http://www.g-octave.org/trac/register
.. _`g-Octave project page`: http://www.g-octave.org/trac/

Now you're done with the configuration.


Running the script
------------------

Update the package database::

    # g-octave --sync

Make sure that you have activated all the ``USE`` flags needed on octave::

    # emerge -vp octave

And build it first::

    # emerge octave

Now that you already have the main dependency of the packages installed
and g-Octave configured, you can run the script::
    
    # /usr/share/g-octave/contrib/manage_pkgdb.py

The packages are installed with the ``--oneshot`` option. To remove them
with the dependencies, run::

    # emerge -av --depclean


Umounting filesystems/directories
---------------------------------

::
    
    # exit
    # cd
    # umount /home/user/g-octave/{proc,dev,usr/portage}
