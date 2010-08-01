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

from __future__ import absolute_import

__all__ = [
    'Description',
    'SvnDescription',
    're_depends',
    're_pkg_atom'
]

import os
import re
import shutil
import tempfile

from contextlib import closing

from .config import Config
from .exception import ConfigException, DescriptionException
from .compat import py3k

if py3k:
    import urllib.request as urllib
else:
    import urllib2 as urllib

from .log import Log
log = Log('g_octave.description')

# octave-forge DESCRIPTION's dependencies atoms
re_depends = re.compile(r'^([a-zA-Z0-9-]+) *(\( *([><=]?=?) *([0-9.]+) *\))?')

# we'll use atoms like 'control-1.0.11' to g-octave packages
re_pkg_atom = re.compile(r'^(.+)-([0-9.]+)$') 

class Description(object):

    def __init__(self, file, conf=None, parse_sysreq=True):
        
        log.info('Parsing file: %s' % file)
        
        if conf is None:
            conf = Config()
        self._config = conf

        if not os.path.exists(file):
            log.error('File not found: %s' % file)
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

                    # comments (started with '#')
                    if line[0] == '#':
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
            if key in ('systemrequirements', 'buildrequires') and parse_sysreq:
                self._desc[key] = self._parse_depends(self._desc[key])


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

                try:
                    conf_dependencies = self._config.dependencies
                except ConfigException:
                    conf_dependencies = {}

                # as octave is already in the portage tree, the atom is
                # predefined.
                if name.lower() == 'octave':
                    atom += 'sci-mathematics/octave'

                elif name in conf_dependencies:
                    if conf_dependencies[name] == '':
                        continue
                    atom += conf_dependencies[name]

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
                log.error('Invalid dependency atom: %s' % depend)
                raise DescriptionException('Invalid dependency atom: %s' % depend)

        return list(set(depends_list))


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
                if name.lower() != 'octave':
                    depends_list.append((name, comparator, version))

            # invalid dependency atom
            else:
                log.error('Invalid dependency atom: %s' % depend)
                raise DescriptionException('Invalid dependency atom: %s' % depend)

        return depends_list


    def __getattr__(self, name):
        """method that overloads the object atributes, returning the needed
        atribute based on the dict with the previously parsed content.
        """

        return self._desc.get(name, None)


class SvnDescription(Description):
    
    _url = 'https://octave.svn.sourceforge.net/svnroot/octave/trunk/octave-forge'
    
    def __init__(self, category, package):
        temp_desc = config_file = tempfile.mkstemp()[1]
        desc_url = '%s/%s/%s/DESCRIPTION' % (
            self._url,
            category,
            package,
        )
        try:
            with closing(urllib.urlopen(desc_url)) as fp:
                with open(temp_desc, 'wb') as fp_:
                    shutil.copyfileobj(fp, fp_)
        except:
            raise DescriptionException('Failed to fetch DESCRIPTION file from SVN')
        Description.__init__(self, temp_desc, parse_sysreq=True)
        os.unlink(temp_desc)
