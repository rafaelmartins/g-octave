#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        fp = open(os.path.join(conf.db, 'update.json'))
        update = fp.read()
        fp.close()
    else:
        fp = open(os.path.join(conf.db, 'update.json'), 'w', 0644)
        fp.write(update)
        fp.close()
    
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
            fp = open(os.path.join(dest, my_file), 'w', 0644)
            fp.write(file_content)
            fp.close()
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
        fp = open(my_file)
        files = json.load(fp)
        fp.close()
    except:
        files = {'files': {}}
    
    for f in re_files:
        if re_files[f].match(_file) != None:
            files['files'][f] = _file
    
    fp = open(my_file, 'w', 0644)
    json.dump(files, fp)
    fp.close()


def check_db_cache():
    
    try:
        fp = open(os.path.join(conf.db, 'cache.json'))
        cache = json.load(fp)
        fp.close()
    except:
        cache = {'files': []}
    
    fp = open(os.path.join(conf.db, 'update.json'))
    update = json.load(fp)
    fp.close()
    
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


if __name__ == '__main__':
    download_files(check_updates())
