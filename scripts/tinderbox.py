#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    tinderbox.py
    ~~~~~~~~~~~~
    
    a simple script that tries to build all the packages in the package
    database and report possible build errors.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import sys
import os

# This block ensures that ^C interrupts are handled quietly.
# Code snippet from Portage
try:
    import signal

    def exithandler(signum,frame):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        sys.exit(1)

    signal.signal(signal.SIGINT, exithandler)
    signal.signal(signal.SIGTERM, exithandler)

except KeyboardInterrupt:
    sys.exit(1)

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(current_dir, '..', 'g_octave')):
    sys.path.insert(0, os.path.join(current_dir, '..'))

import subprocess

from g_octave import config, description_tree, ebuild, fetch, overlay

def build_package(pkgatom):
    proc = subprocess.call([
        'emerge',
        '--nodeps',
        '--nospinner',
        '--verbose',
        '--oneshot',
        pkgatom
    ])
    if proc != os.EX_OK:
        bug_report(pkgatom)
        return False
    return True


def remove_packages(pkglist):
    proc = subprocess.call([
        'emerge',
        '--unmerge',
        pkglist
    ])
    return proc == os.EX_OK
    

def bug_report(pkgatom):
    pass


def main(argv):
    fetch.check_db_cache()
    conf = config.Config()
    
    # creating the overlay
    overlay.create_overlay()
    
    desc_tree = description_tree.DescriptionTree()
    
    # creating the ebuilds for all the packages
    for pkgatom in desc_tree.packages():
        e = ebuild.Ebuild(pkgatom)
        try:
            e.create(nodeps=True)
        except:
            pass
    
    installed_packages = []
    
    try:
        for pkgatom in desc_tree.packages():
            if build_package('=g-octave/'+pkgatom):
                installed_packages.append('=g-octave/'+pkgatom)
    except:
        pass
    finally:
        remove_packages(installed_packages)
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
