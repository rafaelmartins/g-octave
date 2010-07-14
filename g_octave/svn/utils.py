# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~

    This module implements some helper functions to work with SVN packages.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from __future__ import print_function

import sys
import tarfile

from contextlib import closing

def create_tarball(src_dir, tarball_file, arcname):
    
    def exclude(filename):
        return ('.svn' in filename) or ('autom4te.cache' in filename)
    
    try:
        with closing(tarfile.open(tarball_file, 'w:gz')) as tar:
            tar.add(src_dir, arcname=arcname, recursive=True, exclude=exclude)
    except tarfile.TarError as err:
        print('Failed to create the tarball: %s' % err, file=sys.stderr)
