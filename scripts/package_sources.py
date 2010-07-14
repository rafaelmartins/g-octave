#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    package_sources.py
    ~~~~~~~~~~~~~~~~~~
    
    a simple script that create stable source tarballs from the octave-forge
    SVN repository.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from __future__ import print_function

import datetime
import os
import shutil
import sys
import tempfile

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(current_dir, '..', 'g_octave')):
    sys.path.insert(0, os.path.join(current_dir, '..'))

from g_octave import config, description
from g_octave.svn import client, utils

def main(argv):
    conf = config.Config()
    svn = client.SvnClient(create_revisions=False, verbose=True)
    
    # create temporary stuff
    temp_dir = tempfile.mkdtemp()
    
    try:
        checkout_dir = os.path.join(temp_dir, 'checkout')
        error = []
        for category, pkg in svn.update_revisions():
            cur_checkout_dir = os.path.join(checkout_dir, pkg)
            os.makedirs(cur_checkout_dir)
            print('Checking out the package: %s/%s' % (category, pkg))
            try:
                svn.checkout_package(category, pkg, cur_checkout_dir, stable=True)
            except Exception as err:
                error.append('%s/%s' % (category, pkg))
                print('An error was ocurred: %s' % err)
                continue
            
            print('Creating the tarball: %s/%s' % (category, pkg))
            desc = description.Description(os.path.join(cur_checkout_dir, 'DESCRIPTION'))
            new_checkout = os.path.join(temp_dir, '%s-%s' % (pkg, desc.version))
            shutil.move(cur_checkout_dir, new_checkout)
            utils.create_tarball(
                new_checkout,
                # using gzip for backward compatibility
                '%s/%s-%s.tar.gz' % (conf.pkg_cache, pkg, desc.version),
                '%s-%s' % (pkg, desc.version)
            )
    except Exception as err:
        raise RuntimeError('An error was ocurred: %s' % err)
    finally:
        shutil.rmtree(temp_dir)
    if len(error) > 0:
        print('Errors: %s' % ', '.join(error))
            

if __name__ == '__main__':
    sys.exit(main(sys.argv))
