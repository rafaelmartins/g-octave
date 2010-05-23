#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    description.py
    ~~~~~~~~~~~~~~
    
    This module implements a Python object with the content of a given
    DESCRIPTION file.
    
    DESCRIPTION files are basically key/value files with multi-line support.
    The separator is a ':'.
    
    :copyright: (c) 2009-2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

__all__ = [
    'Description',
    're_depends',
    're_atom',
    're_pkg_atom'
]

import re
import os

from config import Config
conf = Config()

# octave-forge DESCRIPTION's dependencies atoms
re_depends = re.compile(r'([a-zA-Z]+) *(\( *([><=]?=?) *([0-9.]+) *\))?')

# we'll use atoms like 'control-1.0.11' to g-octave packages
re_pkg_atom = re.compile(r'^(.+)-([0-9.]+)$')

from exception import DescriptionException

class Description(object):
    
    def __init__(self, file):
        
        if not os.path.exists(file):
            raise DescriptionException('File not found: %s' % file)
        
        # dictionary with the parsed content of the DESCRIPTION file
        self._desc = dict()
        
        # current key
        key = None
        
        with open(file, 'r') as fp:
            for line in fp:
                line_splited = line.split(':')
                
                # 'key: value' found?
                if len(line_splited) >= 2:
                    
                    # by default we have a key before the first ':'
                    key = line_splited[0].strip().lower()
                    
                    # all the stuff after the first ':' is the value
                    # ':' included.
                    value = ':'.join(line_splited[1:]).strip()
                    
                    # the key already exists?
                    if key in self._desc:
                        
                        # it's one of the dependencies?
                        if key in ('depends', 'systemrequirements', 'buildrequires'):
                            
                            # use ', ' to separate the values
                            self._desc[key] += ', '
                        
                        else:
                            
                            # use a single space to separate the values
                            self._desc[key] += ' '
                    
                    # key didn't exists yet. initializing...
                    else:
                        self._desc[key] = ''
                    
                    self._desc[key] += value
                
                # it's not a 'key: value', so it's probably a continuation
                # of the previous line.
                else:
                    
                    # empty line
                    if len(line) == 0:
                        continue
                    
                    # line continuations starts with a single space
                    if line[0] != ' ':
                        continue
                    
                    # the first line can't be a continuation, obviously :)
                    if key is None:
                        continue
                    
                    # our line already have a single space at the start.
                    # we only needs strip spaces at the end of the line
                    self._desc[key] += line.rstrip()
        
        # add the 'self_depends' key
        self._desc['self_depends'] = list()
        
        # parse the dependencies
        for key in self._desc:
            
            # depends
            if key == 'depends':
                depends = self._desc[key]
                self._desc[key] = self._parse_depends(depends)
                self._desc['self_depends'] = self._parse_self_depends(depends)
            
            # requirements
            if key in ('systemrequirements', 'buildrequires'):
                self._desc[key] = self._parse_requirements(self._desc[key])

    
    def _parse_depends(self, depends):
        """returns a list with gentoo atoms for the 'depends' (the other
        octave-forge packages or the octave itself)
        """
        
        # the list that will be returned
        depends_list = list()
        
        for depend in depends.split(','):
            
            # use the 're_depends' regular expression to filter the
            # package name, the version an the comparator
            re_match = re_depends.match(depend.strip())
            
            # the depend is valid?
            if re_match is not None:
                
                # initialize the atom string empty
                atom = ''
                
                # extract the needed values
                name = re_match.group(1)
                comparator = re_match.group(3)
                version = re_match.group(4)
                
                # we have a comparator and a version?
                if comparator is not None and version is not None:
                    
                    # special case: '==' for octave forge is '=' for gentoo
                    if comparator == '==':
                        atom += '='
                    else:
                        atom += comparator
                
                # as octave is already in the portage tree, the atom is
                # predefined.
                if name == 'octave':
                    atom += 'sci-mathematics/octave'
                
                # the octave-forge packages will be put inside a "fake"
                # category: g-octave
                else:
                    atom += 'g-octave/' + str(name)
                
                # append the version to the atom, if needed
                if comparator is not None and version is not None:
                    atom += '-' + str(version)
                
                depends_list.append(atom)
            
            # invalid dependency atom
            else:
                raise DescriptionException('Invalid dependency atom: %s' % depend)
        
        return depends_list
    
    
    def _parse_self_depends(self, depends):
        """returns a list of tuples (name, comparator, version) for the
        other octave-forge packages.
        """
        
        # the list that will be returned
        depends_list = list()
        
        for depend in depends.split(','):
            
            # use the 're_depends' regular expression to filter the
            # package name, the version an the comparator
            re_match = re_depends.match(depend.strip())
            
            # the depend is valid?
            if re_match is not None:
                
                # extract the needed values
                name = re_match.group(1)
                comparator = re_match.group(3)
                version = re_match.group(4)
                
                # we need only the octave-forge packages, nor octave
                if name != 'octave':
                    depends_list.append((name, comparator, version))
        
        return depends_list
    
    
    def _parse_requirements(self, requirements):
        """returns a list with gentoo atoms for the 'requirements' (the
        dependencies that aren't octave-forge packages nor octave itself),
        based on a external list of dependencies.
        """
        
        # the list that will be returned
        requirements_list = list()
        
        for requirement in [i.strip() for i in requirements.split(',')]:
            
            # check if the requirement is on the external file with the
            # dependencies that aren't octave-forge packages nor octave
            # itself.
            if requirement in conf.dependencies:
                req = conf.dependencies[requirement]
                
                # if is a valid value, append to the list
                if req != '':
                    requirements_list.append(req)
        
        return requirements_list

    
    def __getattr__(self, name):
        """method that overloads the object atributes, returning the needed
        atribute based on the dict with the previously parsed content.
        """
        
        return self._desc.get(name, None)
