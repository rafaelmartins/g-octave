#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
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
import subprocess
import re
import shutil
import tarfile

re_files = {
    'info.json':              re.compile(r'info-([0-9]{8})-([0-9]+)\.json'),
    'octave-forge.eclass':    re.compile(r'octave-forge-([0-9]+)\.eclass'),
    'octave-forge.db.tar.gz': re.compile(r'octave-forge-([0-9]{8})\.db\.tar\.gz'),
    'patches.tar.gz':         re.compile(r'patches-([0-9]{8})-([0-9]+)\.tar\.gz'),
}

def check_updates():
    
    try:
        # we'll use urlopen to do all silensiously and save a subprocess
        fp = urllib2.urlopen(conf.db_mirror+'/update.json')
        my_json = fp.read()
        fp.close()
    
    except:
        # if we already have a file, that's ok
        if not os.path.exists(conf.db+'/update.json'):
            raise FetchException('Unable to get file list from the mirror: %s' % conf.db_mirror)
    
    else:
        fp = open(conf.db+'/update.json', 'w', 0664)
        fp.write(my_json)
        fp.close()
        

def download_files():
    
    fp = open(conf.db+'/update.json')
    files = json.load(fp)
    fp.close()
    
    for _file in files['files']:
        if not os.path.exists(conf.db+'/'+_file):
            download_with_wget(conf.db_mirror+'/'+_file, conf.db+'/'+_file)
            add_file_to_db_cache(_file)


def download_with_wget(url, dest):
    
    # TODO: let the user chooses how to fetch the files
    
    ret = subprocess.call([
        '/usr/bin/wget',
        '-t', '5',
        '-T', '60',
        '--passive-ftp',
        '-O', dest+'.part',
        url,
    ])
    
    if ret != 0:
        raise FetchException('Failed to fetch the file: %s' % url)

    shutil.move(dest+'.part', dest)


def add_file_to_db_cache(_file):
    
    try:
        fp = open(conf.db+'/cache.json')
        files = json.load(fp)
        fp.close()
    except:
        files = {'files': {}}
    
    for f in re_files:
        if re_files[f].match(_file) != None:
            files['files'][f] = _file
    
    fp = open(conf.db+'/cache.json', 'w', 0644)
    json.dump(files, fp)
    fp.close()


def check_db_cache():
    
    try:
        fp = open(conf.db+'/cache.json')
        cache = json.load(fp)
        fp.close()
    except:
        cache = {'files': []}
    
    fp = open(conf.db+'/update.json')
    update = json.load(fp)
    fp.close()
    
    for _file in update['files']:
        if _file not in cache['files']:
            if not os.path.exists(conf.db+'/'+_file):
                download_with_wget(conf.db_mirror+'/'+_file, conf.db+'/'+_file)
            add_file_to_db_cache(_file)
            extract(_file)


def extract(_file):
     
    my_file = conf.db+'/'+_file
    
    if tarfile.is_tarfile(my_file):
        fp = tarfile.open(my_file, 'r:gz')
        fp.extractall(conf.db)
     

if __name__ == '__main__':
    check_updates()
    download_files()
    check_db_cache()
