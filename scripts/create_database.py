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

from g_octave import description
from g_octave.svn import client, revisions

def main(argv):
    if len(argv) != 3:
        print >> sys.stderr, 'You should provide 2 arguments: the cache directory and JSON file'
        return 1
    rev = revisions.Revisions(argv[2])
    svn = client.SvnClient(verbose = True)
    for category in svn.categories:
        for pkg in svn.packages[category]:
            current_dir = os.path.join(argv[1], category, pkg)
            os.makedirs(current_dir)
            try:
                print 'Fetching DESCRIPTION from: %s/%s' % (category, pkg)
                fp = urllib2.urlopen(
                    svn.url + '/' + category + '/' + pkg + '/DESCRIPTION'
                )
                with open(os.path.join(current_dir, 'DESCRIPTION'), 'w') as fp_:
                    shutil.copyfileobj(fp, fp_)
            except urllib2.URLError, err:
                print >> sys.stderr, err
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
