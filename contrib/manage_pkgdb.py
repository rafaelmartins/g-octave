#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    manage_pkgdb.py
    ~~~~~~~~~~~~~~~
    
    a simple script to update a Git repository with a package database.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from __future__ import print_function

import datetime
import feedparser
import optparse
import os
import re
import shutil
import subprocess
import sys
import tarfile
import urllib

from contextlib import closing

class Git:
    
    def __init__(self, repo):
        self._repo = repo

    def __call__(self, args):
        args = args[:]
        args.insert(0, 'git')
        return subprocess.call(args, cwd=self._repo)

re_tarball = re.compile(r'(([^/]+)-([0-9.]+)\.tar\.gz)$')

class SfUpdates:
    
    # feed url from 'http://sourceforge.net/projects/octave/files/Octave%20Forge%20Packages/Individual%20Package%20Releases/'
    feed_url = u'http://sourceforge.net/api/file/index/project-id/2888/mtime/desc/rss?path=%2FOctave%20Forge%20Packages%2FIndividual%20Package%20Releases'
    
    svnroot_url = u'https://octave.svn.sourceforge.net/svnroot/octave/trunk/octave-forge/'
    categories = [u'main', u'extra', u'language', u'nonfree']
    
    def __init__(self, local_dir):
        self._local_dir = local_dir
        self.feed = feedparser.parse(self.feed_url)
        if self.feed.bozo == 1:
            raise self.feed.bozo_exception
        self.entries = self.feed.entries

    def remote_files(self):
        # tarball name: {
        #   name,
        #   version,
        #   download url
        # }
        entries = {}
        for entry in self.entries:
            tarball = re_tarball.search(entry.summary)
            if tarball is not None:
                entries[tarball.group(1)] = {
                    'name': tarball.group(2),
                    'version': tarball.group(3),
                    'url': entry.link,
                }
        return entries
    
    def local_files(self):
        # tarball name: {
        #   name,
        #   version,
        #   category
        # }
        if not os.path.isdir(self._local_dir):
            return {}
        entries = {}
        for category in os.listdir(self._local_dir):
            for tarball in os.listdir(os.path.join(self._local_dir, category)):
                my_tarball = re_tarball.search(unicode(tarball))
                if my_tarball is not None:
                    entries[my_tarball.group(1)] = {
                        'name': my_tarball.group(2),
                        'version': my_tarball.group(3),
                        'category': unicode(category),
                    }
        return entries
    
    def guess_category(self, pkgname):
        for category in self.categories:
            f = urllib.urlopen(self.svnroot_url + '/' + category + '/' + pkgname + '/DESCRIPTION')
            if f.getcode() == 200:
                return category            
    
    def check_updates(self):
        local_files = self.local_files()
        remote_files = self.remote_files()
        for remote in remote_files:
            if remote not in local_files:
                print('update found: %s; ' % remote, end='')
                category = self.guess_category(remote_files[remote]['name'])
                if category is None:
                    remote_name = remote_files[remote]['name'].lower()
                    for local in local_files:
                        local_name = local_files[local]['name'].lower()
                        if remote_name == local_name:
                            category = local_files[local]['category']
                            break
                remote_files[remote]['category'] = category
                print('category: %s' % category)
                if self.download(remote, remote_files[remote]) != os.EX_OK:
                    raise RuntimeError('Failed to download: %s' % remote)
    
    def download(self, tarball_name, entry):
        return subprocess.call([
            'wget',
            '--continue',
            '--output-document', os.path.join(
                    self._local_dir,
                    entry['category'],
                    tarball_name,
                ),
            entry['url']
        ])

    def update_package_database(self, db_dir):
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        local_files = self.local_files()
        for tarball_name in local_files:
            entry = local_files[tarball_name]
            description = os.path.join(
                db_dir,
                'octave-forge',
                entry['category'],
                entry['name'],
                '%s-%s.DESCRIPTION' % (entry['name'], entry['version'])
            )
            if not os.path.exists(description):
                if not os.path.exists(os.path.dirname(description)):
                    os.makedirs(os.path.dirname(description))
                tarball = os.path.join(
                    self._local_dir,
                    entry['category'],
                    tarball_name
                )
                with closing(tarfile.open(tarball, 'r:gz')) as src_tar:
                    to_extract = None
                    for f in src_tar:
                        if f.name.endswith('DESCRIPTION'):
                            to_extract = f
                            break
                    if f is None:
                        print('DESCRIPTION file not found: %s', tarball_name, file=sys.stderr)
                        continue
                    with closing(src_tar.extractfile(f)) as fp_tar:
                        with open(description, 'w') as fp:
                            shutil.copyfileobj(fp_tar, fp)


def main(argv):
    
    parser = optparse.OptionParser(
        usage = '%prog [options] <sources directory> <package database directory>',
        version = 'see g-octave --version',
        description = 'a simple script to update a Git repository with a package database.'
    )
    
    parser.add_option(
        '-c', '--commit',
        action = 'store_true',
        dest = 'commit',
        default = False,
        help = 'commit the changes to the Git repository'
    )
    
    parser.add_option(
        '-p', '--push',
        action = 'store_true',
        dest = 'push',
        default = False,
        help = 'push the changes to the remote Git repository'
    )
    
    options, args = parser.parse_args(argv[1:])
    
    if len(args) != 2:
        print(
            'You need to provide 2 arguments:\n'
            '- the directory where you store the source tarballs\n'
            '- the directory where lives your package database (the git repository)',
            file=sys.stderr
        )
        return os.EX_USAGE
    
    print('* Fetching and parsing the Octave-Forge RSS feed ...')
    sf = SfUpdates(args[0])
    print('* Looking for updates ...')
    sf.check_updates()
    print('* Trying to update the package database ...')
    sf.update_package_database(args[1])
    if options.commit or options.push:
        print('* Trying to commit the changes to the package database Git repository ...')
        git = Git(args[1])
        date = datetime.datetime.utcnow().strftime('%H:%M:%S %Y/%m/%d')
        if git(['add', '.']) == os.EX_OK and \
           git(['commit', '-m', 'Package database update - %s' % date]) == os.EX_OK:
            if options.push:
                print('Trying to push the changes to the remote Git repository ...')
                return git(['push'])
            return os.EX_OK
        return os.EX_SOFTWARE
    return os.EX_OK
            

if __name__ == '__main__':
    sys.exit(main(sys.argv))
