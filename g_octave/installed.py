# -*- coding: utf-8 -*-

"""
    installed.py
    ~~~~~~~~~~~~

    This module implements a Python object with the register of g-octave
    installed packages, something like the portage's world file.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import json

class Installed(object):
    
    # this will not be changed by the config file, because the user will
    # lost track of the installed packages if he touch in the location
    # of this file without move it.
    _file = '/var/cache/g-octave.json'
    
    def _load_json(self):
        content = {}
        try:
            with open(self._file) as fp:
                content = json.load(fp)
        except:
            return {}
        return content
    
    def _dump_json(self, content):
        try:
            with open(self._file, 'w') as fp:
                json.dump(content, fp)
        except:
            return False
        return True
            
    def do_install(self, package, version):
        packages = self._load_json()
        packages[package] = version
        if not self._dump_json(packages):
            raise RuntimeError('Failed to save JSON file.')
    
    def is_installed(self, package):
        packages = self._load_json()
        return package in packages
    
    def get_version(self, package):
        packages = self._load_json()
        return packages.get(package, None)
