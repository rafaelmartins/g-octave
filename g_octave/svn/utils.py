# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~

    This module implements some helper functions to work with SVN packages.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import sys
import tarfile

def create_tarball(src_dir, tarball_file, arcname):
    try:
        tar = tarfile.open(tarball_file, 'w:bz2')
        tar.add(src_dir, arcname=arcname, recursive=True, exclude=lambda x: '.svn' in x)
        tar.close()
    except tarfile.TarError, err:
        print >> sys.stderr, 'Failed to create the tarball: %s' % err
