# -*- coding: utf-8 -*-

"""
    fetch.py
    ~~~~~~~~
    
    This module implements a Python class responsible to fetch and update
    the package database and the auxiliary files.
    
    :copyright: (c) 2009-2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

__all__ = [
    'need_update',
    'check_updates',
    'download_files',
    'check_db_cache',
]

from config import Config
conf = Config(True) # fetch phase

from exception import FetchException

import urllib2
import os
import json
import re
import tarfile
import portage.output

out = portage.output.EOutput()

re_files = {
    'info.json':              re.compile(r'info-([0-9]{8})-([0-9]+)\.json'),
    'octave-forge.eclass':    re.compile(r'octave-forge-([0-9]+)\.eclass'),
    'octave-forge.db.tar.gz': re.compile(r'octave-forge-([0-9]{8})\.db\.tar\.gz'),
    'patches.tar.gz':         re.compile(r'patches-([0-9]{8})-([0-9]+)\.tar\.gz'),
}

def need_update():
    
    return not os.path.exists(os.path.join(conf.db, 'update.json'))


def check_updates():
    
    try:
        update = download_with_urllib2(conf.db_mirror + '/update.json', display_info=False)
    except Exception, error:
        # if we already have a file, that's ok
        if need_update():
            raise FetchException(error)
        with open(os.path.join(conf.db, 'update.json')) as fp:
            update = fp.read()
    else:
        with open(os.path.join(conf.db, 'update.json'), 'w', 0644) as fp:
            fp.write(update)
    
    updated_files = json.loads(update)
    
    old_files = []
    
    for _file in updated_files['files']:
        if not os.path.exists(os.path.join(conf.db, _file)):
            old_files.append(_file)
    
    return old_files


def download_files(files):
    
    for _file in files:
        download_with_urllib2(conf.db_mirror + '/' + _file, conf.db)
        add_file_to_db_cache(_file)
        extract(_file)
    

def download_with_urllib2(url, dest=None, display_info=True):
    
    my_file = os.path.basename(url)
    
    if display_info:
        out.ebegin('Downloading: %s' % my_file)
    try:
        fp = urllib2.urlopen(url)
        file_content = fp.read()
        fp.close()
        if dest != None:
            if not os.path.exists(dest):
                os.makedirs(dest, 0755)
            with open(os.path.join(dest, my_file), 'w', 0644) as fp:
                fp.write(file_content)
        else:
            if display_info:
                out.eend(0)
            return file_content
    except Exception, error:
        if display_info:
            out.eend(1)
        raise Exception('Failed to fetch the file (%s): %s' % (my_file, error))
    else:
        if display_info:
            out.eend(0)


def add_file_to_db_cache(_file):
    
    my_file = os.path.join(conf.db, 'cache.json')
    
    try:
        with open(my_file) as fp:
            files = json.load(fp)
    except:
        files = {'files': {}}
    
    for f in re_files:
        if re_files[f].match(_file) != None:
            files['files'][f] = _file
    
    with open(my_file, 'w', 0644) as fp:
        json.dump(files, fp)


def check_db_cache():
    
    try:
        with open(os.path.join(conf.db, 'cache.json')) as fp:
            cache = json.load(fp)
    except:
        cache = {'files': []}
    
    with open(os.path.join(conf.db, 'update.json')) as fp:
        update = json.load(fp)
    
    for _file in update['files']:
        if _file not in cache['files'].values():
            my_file = os.path.join(conf.db, _file)
            if not os.path.exists(my_file):
                download_with_wget(conf.db_mirror + '/' + _file, my_file)
            add_file_to_db_cache(_file)
            extract(_file)


def extract(gz_file, display_info=True):
     
    my_file = os.path.join(conf.db, gz_file)
    
    if tarfile.is_tarfile(my_file):
        if display_info:
            out.ebegin('Extracting: %s' % os.path.basename(gz_file))
        try:
            fp = tarfile.open(my_file, 'r:gz')
            fp.extractall(conf.db)
        except Exception, error:
            if display_info:
                out.eend(1)
            raise Exception('Failed to extract the file (%s): %s' % (my_file, error))
        else:
            if display_info:
                out.eend(0)
