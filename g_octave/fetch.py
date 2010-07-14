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

from __future__ import absolute_import

__all__ = [
    'need_update',
    'check_updates',
    'download_files',
    'check_db_cache',
]

from .config import Config
conf = Config(True) # fetch phase

from .exception import FetchException
from .compat import py3k, open as open_

if py3k:
    import urllib.request as urllib
else:
    import urllib2 as urllib
import os
import json
import re
import shutil
import tarfile
import portage.output

from contextlib import closing

out = portage.output.EOutput()

re_files = {
    'info.json':              re.compile(r'info-([0-9]{10})-([0-9]+)\.json'),
    'octave-forge.db.tar.gz': re.compile(r'octave-forge-([0-9]{10})\.db\.tar\.gz'),
    'patches.tar.gz':         re.compile(r'patches-([0-9]{10})-([0-9]+)\.tar\.gz'),
}

def need_update():
    
    return not os.path.exists(os.path.join(conf.db, 'update.json'))


def check_updates():
    
    try:
        update = download_with_urllib2(
            conf.db_mirror + '/update.json',
            display_info=False
        ).decode('utf-8')
    except Exception as error:
        # if we already have a file, that's ok
        if need_update():
            raise FetchException(error)
        with open_(os.path.join(conf.db, 'update.json')) as fp:
            update = fp.read()
    else:
        with open_(os.path.join(conf.db, 'update.json'), 'w') as fp:
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
        if dest != None:
            with closing(urllib.urlopen(url)) as fp:
                if not os.path.exists(dest):
                    os.makedirs(dest, 0o755)
                with open(os.path.join(dest, my_file), 'wb') as fp_:
                    shutil.copyfileobj(fp, fp_)
        else:
            with closing(urllib.urlopen(url)) as fp:
                if display_info:
                    out.eend(0)
                return fp.read()
    except Exception as error:
        if display_info:
            out.eend(1)
        raise Exception('Failed to fetch the file (%s): %s' % (my_file, error))
    else:
        if display_info:
            out.eend(0)


def add_file_to_db_cache(_file):
    
    my_file = os.path.join(conf.db, 'cache.json')
    
    try:
        with open_(my_file) as fp:
            files = json.load(fp)
    except:
        files = {'files': {}}
    
    for f in re_files:
        if re_files[f].match(_file) != None:
            files['files'][f] = _file
    
    with open_(my_file, 'w') as fp:
        json.dump(files, fp)


def check_db_cache():
    
    try:
        with open_(os.path.join(conf.db, 'cache.json')) as fp:
            cache = json.load(fp)
    except:
        cache = {'files': {}}
    
    try:
        with open_(os.path.join(conf.db, 'update.json')) as fp:
            update = json.load(fp)
    except:
        my_cache = os.listdir(conf.db)
        update = {'files': []}
        for f in my_cache:
            for s in ['patches-', 'info-', 'octave-forge-']:
                if f.startswith(s) and f not in update['files']:
                    update['files'].append(f)
    
    for _file in update['files']:
        if _file not in list(cache['files'].values()):
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
        except Exception as error:
            if display_info:
                out.eend(1)
            raise Exception('Failed to extract the file (%s): %s' % (my_file, error))
        else:
            if display_info:
                out.eend(0)
