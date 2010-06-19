#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    create_database.py
    ~~~~~~~~~~~~~~~~~~
    
    a simple script that builds a package database from the octave-forge
    SVN repository.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import shutil
import sys
import tempfile
import urllib2

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(current_dir, '..', 'g_octave')):
    sys.path.insert(0, os.path.join(current_dir, '..'))

from g_octave import config, description
from g_octave.svn import client, utils

def main(argv):
    #if len(argv) != 3:
    #    print >> sys.stderr, 'You should provide 2 arguments: the cache directory and JSON file'
    #    return 1
    conf = config.Config()
    svn = client.SvnClient(create_revisions=False, verbose=True)
    
    # create temporary stuff
    temp_dir = tempfile.mkdtemp()
    checkout_dir = os.path.join(temp_dir, 'checkout')
    db_dir = os.path.join(temp_dir, 'db')
    
    for category, pkg in svn.update_revisions():
        cur_checkout_dir = os.path.join(checkout_dir, pkg)
        os.makedirs(cur_checkout_dir)
        while 1:
            print 'Checking out the package: %s/%s' % (category, pkg)
            if svn.checkout_package(category, pkg, cur_checkout_dir, stable=True):
                break
            print 'An error was ocurred. Retrying ...'
        
        # copying DESCRIPTION file for the package database
        cur_db_dir = os.path.join(db_dir, category, pkg)
        os.makedirs(cur_db_dir)
        shutil.copy(
            os.path.join(cur_checkout_dir, 'DESCRIPTION'),
            os.path.join(cur_db_dir, 'DESCRIPTION'),
        )
        
        print 'Creating the tarball: %s/%s' % (category, pkg)
        desc = description.Description(os.path.join(cur_db_dir, 'DESCRIPTION'))
        new_checkout = os.path.join(temp_dir, '%s-%s' % (pkg, desc.version))
        shutil.move(cur_checkout_dir, new_checkout)
        utils.create_tarball(
            new_checkout,
            '%s-%s.tar.bz2' % (pkg, desc.version),
            '%s-%s' % (pkg, desc.version)
        )
            

if __name__ == '__main__':
    sys.exit(main(sys.argv))
