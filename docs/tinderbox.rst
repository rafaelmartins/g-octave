Tinderbox
=========

g-Octave provides a script to run build tests for all the octave-forge
packages. This script is not intended to be used by end-users, only
developers.

.. topic:: Warning!

    The automated bug reports are broken right now, because the Trac instance
    is currently offline and being moved to the Gentoo Linux infrastructure.


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

You should mount your current ``/usr/portage`` inside the chroot dir::

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
    # emerge -av mercurial pycurl


Getting the source code
-----------------------

Using the Git repository::
    
    # cd
    # git clone git://git.overlays.gentoo.org/proj/g-octave.git
    # cd g-octave


Using the source tarball::
    
    # cd
    # wget http://files.rafaelmartins.eng.br/distfiles/g-octave/g-octave-<VERSION>.tar.gz
    # tar xvzf g-octave-<VERSION>.tar.gz
    # cd g-octave-<VERSION>


Configuring g-Octave
--------------------

::

    # cp etc/g-octave.cfg /etc

.. topic:: Warning!

    This is currently broken!

You should edit the file ``/etc/g-octave.cfg`` and append the lines below
(with your data)::

    trac_user = username
    trac_passwd = password

For this you'll need to register_ at the `g-Octave project page`_, in order
to be able to create new tickets and attachments.

.. _register: http://g-octave.rafaelmartins.eng.br/register
.. _`g-Octave project page`: http://g-octave.rafaelmartins.eng.br/

Now you need to add the g-octave overlay to the Portage configuration file
``/etc/make.conf`` (use the same overlay path from ``/etc/g-octave.cfg``)::

    # echo 'PORTDIR_OVERLAY="/usr/local/portage/g-octave ${PORTDIR_OVERLAY}" >> /etc/make.conf


Running the script
------------------

Update the package database::

    # ./scripts/g-octave --sync

Run the test suites::

    # ./scripts/run_tests.py

Make sure that you have activated all the ``USE`` flags needed by octave::

    # emerge -vp octave

Run the script::
    
    # ./scripts/tinderbox.py

At the end, the script should uninstall all the octave-forge packages
directly installed. If you want to remove the dependencies, run::

    # emerge -av --depclean


Umounting filesystems/directories
---------------------------------

::
    
    # exit
    # cd
    # umount /home/user/g-octave/{proc,dev,usr/portage}
