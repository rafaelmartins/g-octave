#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['create_overlay']

from config import Config
conf = Config()

import os
import shutil

def create_overlay(force=False):
    
    if force:
        if os.path.exists(conf.overlay):
            shutil.rmtree(conf.overlay)
    
    # creating dirs
    for _dir in ['profiles', 'eclass']:
        dir = os.path.join(conf.overlay, _dir)
        if not os.path.exists(dir) or force:
            os.makedirs(dir, 0755)
    
    # creating files
    files = {
        os.path.join(conf.overlay, 'profiles', 'repo_name'): 'g-octave',
        os.path.join(conf.overlay, 'profiles', 'categories'): 'g-octave',
        os.path.join(conf.overlay, 'eclass', 'octave-forge.eclass'):
            open(os.path.join(conf.db, conf.cache['octave-forge.eclass'])),
    }
    for _file in files:
        if not os.path.exists(_file) or force:
            __create_file(_file, files[_file])


def __create_file(_file, content):
    
    if type(content) == file:
        content = content.read()
    
    fp = open(_file, 'w', 0644)
    fp.write(content)
    fp.close()
    
    type(content) == file and content.close()


if __name__ == '__main__':
    create_overlay(True)
