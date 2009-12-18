#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from description import *
import re

class EbuildException(Exception):
    pass

class Ebuild:
    
    def __init__(self, pkg_atom):
        
        atom = re_pkg_atom.match(pkg_atom)
        if atom == None:
            raise EbuildException('Invalid Atom: %s' % pkg_atom)
        
        self.pkgname = atom.group(1)
        
        # any version required?
        if atom.group(2) != None:
            # check if the version is available
            pass
        else:
            # check the latest version available
            pass
        
        print atom.groups()

if __name__ == '__main__':
    a = Ebuild('missing-functions-1.0.2')
