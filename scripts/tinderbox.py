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

import csv
import portage
import subprocess
import urllib
import urllib2

from g_octave import config, description_tree, ebuild, fetch, overlay
from g_octave.tinderbox.trac import Trac

trac = None

def build_package(pkgatom):
    proc = subprocess.call([
        'emerge',
        #'--nodeps',
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
    ] + pkglist)
    return proc == os.EX_OK
    

def bug_report(pkgatom):
    
    bug_id = None
    
    # already have a ticket for this package?
    for row in trac.list_tickets('=g-octave/'+ pkgatom + ' fails to build. #tinderbox'):
        bug_id = row['id']
    
    # if not exists a ticket, create one
    if bug_id is None:
        bug_id = trac.create_ticket(
            '=g-octave/'+ pkgatom + ' fails to build. #tinderbox',
            'This is ticket was created by tinderbox.\nLook at the attachments.'
        )
        bug_id = int(bug_id)
    
    # attach the build.log and the environment
    tmpdir = os.path.join(
        portage.settings['PORTAGE_TMPDIR'],
        'portage',
        'g-octave',
        pkgatom,
        'temp'
    )
    
    for f in ['build.log', 'environment']:
        # curl hates utf-8
        f_ = str(os.path.join(tmpdir, f))
        if os.path.exists(f_):
            trac.attach_file(bug_id, '%s file.' % f, f_)
        else:
            print >> sys.stderr, f_ + ' don\'t exists!'

        
def main(argv):
    global trac
    
    fetch.check_db_cache()
    conf = config.Config()
    
    trac = Trac(conf.trac_user, conf.trac_passwd)
    
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
            if build_package(pkgatom):
                installed_packages.append('=g-octave/'+pkgatom)
    except:
        pass
    finally:
        remove_packages(installed_packages)
    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
