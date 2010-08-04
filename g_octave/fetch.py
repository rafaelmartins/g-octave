# -*- coding: utf-8 -*-

"""
    fetch.py
    ~~~~~~~~
    
    This module implements a Python class responsible to fetch and update
    the package database and the auxiliary files.
    
    Used only by the live version of g-octave.
    
    :copyright: (c) 2009-2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from __future__ import absolute_import, print_function

__all__ = ['fetch']

from .config import Config
conf = Config(True) # fetch phase

from .exception import FetchException
from .compat import py3k, open as open_

if py3k:
    import urllib.request as urllib
else:
    import urllib2 as urllib

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile

from contextlib import closing

def clean_db():
    for f in ['timestamp', 'info.json', 'patches', 'octave-forge']:
        current = os.path.join(conf.db, f)
        if os.path.isdir(current):
            shutil.rmtree(current)
        elif os.path.isfile(current):
            os.unlink(current)

class GitHub:
    
    re_db_mirror = re.compile(r'github://(?P<user>[^/]+)/(?P<repo>[^/]+)/?')
    
    def __init__(self, user, repo):
        self.user = user
        self.repo = repo
        self.api_url = 'http://github.com/api/v2/json'
        self.url = 'http://github.com'
    
    def need_update(self):
        return not os.path.exists(os.path.join(
            conf.db, 'cache', 'commit_id'
        ))
    
    def get_commits(self, branch='master'):
        url = '%s/commits/list/%s/%s/%s/' % (
            self.api_url,
            self.user,
            self.repo,
            branch
        )
        commits = {}
        with closing(urllib.urlopen(url)) as fp:
            commits = json.load(fp)
        return commits['commits']
    
    def fetch_db(self, branch='master'):
        cache = os.path.join(conf.db, 'cache')
        commit_id = os.path.join(cache, 'commit_id')
        if not os.path.exists(cache):
            os.makedirs(cache)
        last_commit = self.get_commits()[0]['id']
        if os.path.exists(commit_id):
            with open_(commit_id) as fp:
                if fp.read().strip() == last_commit:
                    return False
        dest = os.path.join(cache, 'octave-forge-%s.tar.gz' % last_commit)
        return_value = subprocess.call([
            'wget',
            '--continue',
            '--output-document', dest,
            '%s/%s/%s/tarball/%s/' % (
                self.url,
                self.user,
                self.repo,
                branch
            )
        ])
        if return_value == os.EX_OK:
            with open_(os.path.join(cache, 'commit_id'), 'w') as fp:
                fp.write(last_commit)
        return True

    def extract(self):
        clean_db()
        cache = os.path.join(conf.db, 'cache')
        commit_id = os.path.join(cache, 'commit_id')
        tarball = None
        if os.path.exists(commit_id):
            with open_(commit_id) as fp:
                tarball = os.path.join(
                    cache,
                    'octave-forge-%s.tar.gz' % fp.read().strip()
                )
        if tarball is not None:
            if tarfile.is_tarfile(tarball):
                with closing(tarfile.open(tarball, 'r')) as fp:
                    fp.extractall(conf.db)
                dirs = glob.glob('%s/%s-%s*' % (conf.db, self.user, self.repo))
                if len(dirs) != 1:
                    raise FetchException('Failed to extract the tarball.')
                    return
                for f in os.listdir(dirs[0]):
                    shutil.move(os.path.join(dirs[0], f), conf.db)
                os.rmdir(dirs[0])

# TODO: Implement gitweb support

__modules__ = [
    GitHub
]

def fetch():
    for module in __modules__:
        match = module.re_db_mirror.match(conf.db_mirror)
        if match is not None:
            return module(**match.groupdict())
