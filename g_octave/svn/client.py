# -*- coding: utf-8 -*-

"""
    client.py
    ~~~~~~~~~

    This module implements a interface between g-octave and the octave-forge
    Subversion repository.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from __future__ import print_function, absolute_import

import os
import pysvn
import re
import shutil
import subprocess
import sys

from g_octave.compat import py3k

if py3k:
    import urllib.request as url_request, urllib.error as url_error
else:
    import urllib2
    url_request = urllib2
    url_error = urllib2

from contextlib import closing

from . import revisions
from g_octave import config

class SvnClient:
    
    url = 'https://octave.svn.sourceforge.net/svnroot/octave/trunk/octave-forge/'
    categories = ['main', 'extra', 'language', 'nonfree']
    exclude = ['CONTENTS', 'INDEX', 'Makefile', 'base']
    
    def __init__(self, create_revisions=True, verbose=False):
        self.conf = config.Config()
        json_file = os.path.join(self.conf.db, 'revisions.json')
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
        pkg_cache_dir = self.conf.pkg_cache
        try:
            pkg_cache = os.listdir(pkg_cache_dir)
        except:
            raise RuntimeError('Failed to list packages from the pkg_cache')
        for category in self.categories:
            self.packages[category] = self._list_packages(category)
        for category in self.packages:
            for package in self.packages[category]:
                old_revision = self._revisions.get(category, package)
                current_revision = self.packages[category][package]
                tarball_exist = False
                for package_c in pkg_cache:
                    if re.match(r'%s\-[0-9\.]+' % package, package_c) is not None:
                        tarball_exist = True
                if current_revision is None or old_revision is None or current_revision > old_revision or not tarball_exist:
                    self._revisions.set(category, package, current_revision)
                    updated.append((category, package))
        return updated

    def _list_packages(self, category):
        try:
            if self._verbose:
                print('Listing packages from: ' + category)
            pkg_list = self._client.list(
                self.url + '/' + category + '/',
                depth = pysvn.depth.immediates
            )
        except pysvn.ClientError as err:
            print('Error: ' + str(err), file=sys.stderr)
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
                        print('Fetching DESCRIPTION from: %s/%s' % (category, pkg))
                    fp = url_request.urlopen(
                        self.url + '/' + category + '/' + pkg + '/DESCRIPTION'
                    )
                    with open(os.path.join(current_dir, 'DESCRIPTION'), 'wb') as fp_:
                        shutil.copyfileobj(fp, fp_)
                except url_error.URLError:
                    pass

    def checkout_package(self, category, name, dest, stable=True):
        if stable:
            # get DESCRIPTION revision
            info = self._client.info2(
                self.url + '/' + category + '/' + name + '/DESCRIPTION'
            )
            revision = info[0][1].last_changed_rev
        self._client.checkout(
            self.url + '/' + category + '/' + name + '/',
            dest,
            revision = stable and revision or \
                pysvn.Revision(pysvn.opt_revision_kind.head)
        )
        makefile = os.path.join(dest, 'Makefile')
        configure = os.path.join(dest, 'configure')
        autogen = os.path.join(dest, 'src', 'autogen.sh')
        self.download_file('packages/package_Makefile.in', os.path.join(dest, 'Makefile'))
        self.download_file('packages/package_configure.in', configure)
        os.chmod(configure, 0o755)
        if os.path.exists(autogen):
            os.chmod(autogen, 0o755)
            if subprocess.call(
                'cd %s && ./autogen.sh' % os.path.dirname(autogen),
                shell=True
            ) != os.EX_OK:
                raise RuntimeError('Failed to run autogen.sh')
    
    def download_file(self, src, dest):
        with closing(url_request.urlopen(self.url + '/' + src)) as fp:
            with open(dest, 'wb') as fp_:
                shutil.copyfileobj(fp, fp_)
