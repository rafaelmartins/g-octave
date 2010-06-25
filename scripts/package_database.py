#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    package_database.py
    ~~~~~~~~~~~~~~~~~~~
    
    a simple script that create a package database from the octave-forge
    SVN repository.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(current_dir, '..', 'g_octave')):
    sys.path.insert(0, os.path.join(current_dir, '..'))

import shutil
import tarfile
import tempfile

from contextlib import closing

from g_octave import config
from g_octave.svn import revisions, utils

def main(argv):
    conf = config.Config()
    json_file = os.path.join(conf.db, 'revisions.json')
    db = revisions.Revisions(json_file).get()
    pkg_cache = os.listdir(conf.pkg_cache)
    temp_dir = tempfile.mkdtemp()
    try:
        for category in db:
            category_dir = os.path.join(temp_dir, category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
            for package in db[category]:
                for tarball in pkg_cache:
                    if tarball.startswith(package + '-') and tarball.endswith('.tar.gz'):
                        dirname = tarball[:tarball.find('.tar.gz')]
                        tarball_path = os.path.join(conf.pkg_cache, tarball)
                        with closing(tarfile.open(tarball_path, 'r:gz')) as src_tar:
                            src_tar.extract(
                                os.path.join(dirname, 'DESCRIPTION'),
                                path = category_dir
                            )
        utils.create_tarball(temp_dir, argv[1], 'octave-forge')
    except Exception, err:
        raise RuntimeError('An error was ocurred: %s' % err)
    finally:
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
