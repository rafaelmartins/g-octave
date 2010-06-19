# -*- coding: utf-8 -*-

"""
    client.py
    ~~~~~~~~~

    This module implements a interface between g-octave and the octave-forge
    Subversion repository.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import pysvn
import shutil
import subprocess
import sys
import urllib2

import revisions

from g_octave import config

class SvnClient:
    
    url = 'https://octave.svn.sourceforge.net/svnroot/octave/trunk/octave-forge/'
    categories = ['main', 'extra', 'language', 'nonfree']
    exclude = ['CONTENTS', 'INDEX', 'Makefile', 'base']
    
    def __init__(self, create_revisions=True, verbose=False):
        conf = config.Config()
        json_file = os.path.join(conf.db, 'revisions.json')
        self._verbose = verbose
        self._client = pysvn.Client()
        self._revisions = revisions.Revisions(json_file)
        self.packages = {}
        if create_revisions and not os.path.exists(json_file):
            self.update_revisions()
        else:
            self.packages = self._revisions.get()

    def update_revisions(self):
        updated = []
        for category in self.categories:
            self.packages[category] = self._list_packages(category)
        for category in self.packages:
            for package in self.packages[category]:
                old_revision = self._revisions.get(category, package)
                current_revision = self.packages[category][package]
                if current_revision is None or current_revision > old_revision:
                    self._revisions.set(category, package, current_revision)
                    updated.append((category, package))
        return updated

    def _list_packages(self, category):
        try:
            if self._verbose:
                print 'Listing packages from: ' + category
            pkg_list = self._client.list(
                self.url + '/' + category + '/',
                depth = pysvn.depth.immediates
            )
        except pysvn.ClientError, err:
            print >> sys.stderr, 'Error: ' + str(err)
        tmp = {}
        for props, lock in pkg_list:
            filename = props.repos_path.split('/')[-1]
            if filename not in self.exclude and filename != category:
                tmp[filename] = props.created_rev.number
        return tmp

    def create_description_tree(self, dest, categories=['main', 'extra', 'language']):
        for category in categories:
            if category not in self.categories:
                continue
            for pkg, revision in self.packages[category]:
                current_dir = os.path.join(dest, category, pkg)
                os.makedirs(current_dir)
                try:
                    if self._verbose:
                        print 'Fetching DESCRIPTION from: %s/%s' % (category, pkg)
                    fp = urllib2.urlopen(
                        self.url + '/' + category + '/' + pkg + '/DESCRIPTION'
                    )
                    with open(os.path.join(current_dir, 'DESCRIPTION'), 'w') as fp_:
                        shutil.copyfileobj(fp, fp_)
                except urllib2.URLError:
                    pass

    def checkout_package(self, category, name, dest, stable=True):
        if stable:
            # get DESCRIPTION revision
            try:
                info = self._client.info2(
                    self.url + '/' + category + '/' + name + '/DESCRIPTION'
                )
            except pysvn.ClientError, err:
                return False
            revision = info[0][1].last_changed_rev
        try:
            self._client.checkout(
                self.url + '/' + category + '/' + name + '/',
                dest,
                revision = stable and revision or \
                    pysvn.Revision(pysvn.opt_revision_kind.head)
            )
        except pysvn.ClientError, err:
            return False
        return True
