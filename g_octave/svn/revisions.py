# -*- coding: utf-8 -*-

"""
    revisions.py
    ~~~~~~~~~~~~

    This module implements a Python object with the revisions for each
    package fetched from the octave-forge SVN.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import json

from g_octave.compat import open

class Revisions(object):
    
    def __init__(self, json_file):
        self._file = json_file
    
    def _load_json(self):
        revisions = {}
        try:
            with open(self._file) as fp:
                revisions = json.load(fp)
        except:
            return {}
        return revisions
    
    def _dump_json(self, revisions):
        try:
            with open(self._file, 'w') as fp:
                json.dump(revisions, fp)
        except:
            return False
        return True
            
    def get(self, category=None, package=None):
        revisions = self._load_json()
        if category is None:
            return revisions        
        if category in revisions:
            if package is None:
                return revisions[category]
            if package in revisions[category]:
                return revisions[category][package]
        return None
    
    def set(self, category, package, value):
        revisions = self._load_json()
        if category not in revisions:
            revisions[category] = {}
        revisions[category][package] = value
        if not self._dump_json(revisions):
            raise RuntimeError('Failed to save JSON file.')
