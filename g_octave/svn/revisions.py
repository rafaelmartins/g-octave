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
            
    def __getitem__(self, key):
        revisions = self._load_json()
        if key in revisions:
            return revisions[key]
        return None
    
    def __setitem__(self, key, value):
        revisions = self._load_json()
        revisions[key] = value
        if not self._dump_json(revisions):
            raise RuntimeError('Failed to save JSON file.')

if __name__ == '__main__':
    a = Revisions('/tmp/file.json')
    a['fuuuu'] = 1234
    print a['fuuuu']
            
