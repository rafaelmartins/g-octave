#!/usr/bin/env python
# -*- coding: utf-8 -*-

from description import *
from config import Config
conf = Config()

import os

class DescriptionTreeException(Exception):
    pass

class DescriptionTree(object):
    
    def __init__(self):
        
        self.pkg_list = {}
        
        self.__db_path = conf.db
        
        if not os.path.isdir(self.__db_path):
            raise DescriptionTreeException('Invalid db: %s' % self.__db_path)
        
        for cat in conf.categories:
            catdir = os.path.join(self.__db_path, cat)
            if os.path.isdir(catdir):
                self.pkg_list[cat] = []
                pkgs = os.listdir(catdir)
                for pkg in pkgs:
                    mypkg = re_pkg_atom.match(pkg)
                    if mypkg == None:
                        raise DescriptionTreeException('Invalid Atom: %s' % mypkg)
                    self.pkg_list[cat].append({
                        'name': mypkg.group(1),
                        'version': mypkg.group(2),
                    })
    
    
    def __getitem__(self, key):
        
        mykey = re_pkg_atom.match(key)
        if mykey == None:
            raise DescriptionTreeException('Invalid Atom: %s' % mypkg)
        
        name = mykey.group(1)
        version = mykey.group(2)
        
        for cat in self.pkg_list:
            for pkg in self.pkg_list[cat]:
                if pkg['name'] == name and pkg['version'] == version:
                    pkgfile = os.path.join(
                        self.__db_path,
                        cat,
                        '%s-%s' % (pkg['name'], pkg['version']),
                        'DESCRIPTION'
                    )
                    return Description(pkgfile)
        
        return None


if __name__ == '__main__':
    a = DescriptionTree()
    b = a['bugfix-3.0.6-1.0']
    print b.depends
