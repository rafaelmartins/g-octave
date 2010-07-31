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

from __future__ import absolute_import

__all__ = ['DescriptionTree']

import os
import re

from portage.versions import vercmp

from .config import Config
from .description import *
from .exception import ConfigException, DescriptionTreeException

has_svn = True
try:
    from .svn import *
except ImportError:
    has_svn = False

from .log import Log
log = Log('g_octave.description_tree')

class DescriptionTree(object):
    
    def __init__(self, conf=None, parse_sysreq=True):
        
        log.info('Parsing the package database.')
        
        self._parse_sysreq = parse_sysreq
        self.pkg_list = {}
        
        if conf is None:
            conf = Config()
        self._config = conf
        
        self._db_path = os.path.join(conf.db, 'octave-forge')
        
        if not os.path.isdir(self._db_path):
            log.error('Invalid db: %s' % self._db_path)
            raise DescriptionTreeException('Invalid db: %s' % self._db_path)
        
        self.categories = {}
        for cat in [i.strip() for i in conf.categories.split(',')]:
            catdir = os.path.join(self._db_path, cat)
            if os.path.isdir(catdir):
                self.pkg_list[cat] = []
                pkgs = os.listdir(catdir)
                for pkg in pkgs:
                    pkgdir = os.path.join(catdir, pkg)
                    for desc_file in os.listdir(pkgdir):
                        pkg_p = desc_file[:-len('.DESCRIPTION')]
                        mypkg = re_pkg_atom.match(pkg_p)
                        if mypkg == None:
                            log.error('Invalid Atom: %s' % mypkg)
                            raise DescriptionTreeException('Invalid Atom: %s' % mypkg)
                        try:
                            blacklist = conf.blacklist
                        except ConfigException:
                            # blacklist isn't mandatory
                            blacklist = []
                        if mypkg.group(1) not in blacklist or not parse_sysreq:
                            self.categories[mypkg.group(1)] = cat
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
                        pkg['name'],
                        '%s-%s.DESCRIPTION' % (pkg['name'], pkg['version']),
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
        
        tmp.sort(vercmp)
        return tmp
        
    
    def latest_version(self, pkgname):
        
        tmp = self.package_versions(pkgname)
        return tmp[-1]


    def version_compare(self, versions):
        
        tmp = list(versions[:])
        tmp.sort(vercmp)
        return tmp[-1]

    
    def packages(self):
        
        packages = []
        
        for cat in self.pkg_list:
            for pkg in self.pkg_list[cat]:
                packages.append(pkg['name'] + '-' + pkg['version'])
        
        return packages

    
    def search(self, term):
        
        # term can be a regular expression
        re_term = re.compile(r'%s' % term)
        packages = {}
        
        for cat in self.pkg_list:
            for pkg in self.pkg_list[cat]:
                if re_term.search(pkg['name']) is not None:
                    if pkg['name'] not in packages:
                        packages[pkg['name']] = [pkg['version']]
                        if has_svn:
                            packages[pkg['name']].append('9999')
                    else:
                        packages[pkg['name']].insert(-1, pkg['version'])
        
        return packages

