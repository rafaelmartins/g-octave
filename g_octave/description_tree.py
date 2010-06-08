# -*- coding: utf-8 -*-

"""
    description_tree.py
    ~~~~~~~~~~~~~~~~~~~
    
    This module implements a Python object with the content of a directory
    tree with DESCRIPTION files. The object contains *g_octave.Description*
    objects for each DESCRIPTION file.
    
    :copyright: (c) 2009-2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

__all__ = ['DescriptionTree']

import os

from config import Config
from description import *
from exception import ConfigException, DescriptionTreeException

class DescriptionTree(object):
    
    def __init__(self, conf=None, parse_sysreq=True):
        
        self._parse_sysreq = parse_sysreq
        self.pkg_list = {}
        
        if conf is None:
            conf = Config()
        self._config = conf
        
        self._db_path = os.path.join(conf.db, 'octave-forge')
        
        if not os.path.isdir(self._db_path):
            raise DescriptionTreeException('Invalid db: %s' % self._db_path)
        
        for cat in [i.strip() for i in conf.categories.split(',')]:
            catdir = os.path.join(self._db_path, cat)
            if os.path.isdir(catdir):
                self.pkg_list[cat] = []
                pkgs = os.listdir(catdir)
                for pkg in pkgs:
                    mypkg = re_pkg_atom.match(pkg)
                    if mypkg == None:
                        raise DescriptionTreeException('Invalid Atom: %s' % mypkg)
                    try:
                        blacklist = conf.blacklist
                    except ConfigException:
                        # blacklist isn't mandatory
                        blacklist = []
                    if mypkg.group(1) not in blacklist or not parse_sysreq:
                        self.pkg_list[cat].append({
                            'name': mypkg.group(1),
                            'version': mypkg.group(2),
                        })
    
    
    def __getitem__(self, key):
        
        mykey = re_pkg_atom.match(key)
        if mykey == None:
            return None
        
        name = mykey.group(1)
        version = mykey.group(2)
        
        for cat in self.pkg_list:
            for pkg in self.pkg_list[cat]:
                if pkg['name'] == name and pkg['version'] == version:
                    pkgfile = os.path.join(
                        self._db_path,
                        cat,
                        '%s-%s' % (pkg['name'], pkg['version']),
                        'DESCRIPTION'
                    )
                    return Description(
                        pkgfile,
                        conf = self._config,
                        parse_sysreq = self._parse_sysreq
                    )
        
        return None
    
    
    def package_versions(self, pkgname):
        
        tmp = []
        
        for cat in self.pkg_list:
            for pkg in self.pkg_list[cat]:
                if pkg['name'] == pkgname:
                    tmp.append(pkg['version'])
        
        return tmp
        
    
    def latest_version(self, pkgname):
        
        tmp = self.package_versions(pkgname)
        return self.version_compare(tmp)


    def version_compare(self, versions):
        
        max = ('0',)
        maxstr = None
        
        for version in versions:
            tmp = tuple(version.split('.'))
            if tmp > max:
                max = tmp
                maxstr = version
        
        return maxstr

    
    def packages(self):
        
        packages = []
        
        for cat in self.pkg_list:
            for pkg in self.pkg_list[cat]:
                packages.append(pkg['name'] + '-' + pkg['version'])
        
        return packages
