#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_description.py
    ~~~~~~~~~~~~~~~~~~~

    test suite for the *g_octave.description* module

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import unittest
import utils

from g_octave import description


class TestDescription(unittest.TestCase):

    def setUp(self):
        conf, self._config_file, self._tempdir = utils.create_env()
        self.desc = description.Description(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'files', 'DESCRIPTION',
            ),
            conf = conf
        )

    def test_re_depends(self):
        depends = [
            ('pkg', ('pkg', None, None)),
            ('pkg(<1)', ('pkg', '<', '1')),
            ('pkg(>1)', ('pkg', '>', '1')),
            ('pkg(<=1)', ('pkg', '<=', '1')),
            ('pkg(>=1)', ('pkg', '>=', '1')),
            ('pkg(==1)', ('pkg', '==', '1')),
            ('pkg( <1)', ('pkg', '<', '1')),
            ('pkg( >1)', ('pkg', '>', '1')),
            ('pkg( <=1)', ('pkg', '<=', '1')),
            ('pkg( >=1)', ('pkg', '>=', '1')),
            ('pkg( ==1)', ('pkg', '==', '1')),
            ('pkg(<1 )', ('pkg', '<', '1')),
            ('pkg(>1 )', ('pkg', '>', '1')),
            ('pkg(<=1 )', ('pkg', '<=', '1')),
            ('pkg(>=1 )', ('pkg', '>=', '1')),
            ('pkg(==1 )', ('pkg', '==', '1')),
            ('pkg( <1 )', ('pkg', '<', '1')),
            ('pkg( >1 )', ('pkg', '>', '1')),
            ('pkg( <=1 )', ('pkg', '<=', '1')),
            ('pkg( >=1 )', ('pkg', '>=', '1')),
            ('pkg( ==1 )', ('pkg', '==', '1')),
            ('pkg(<1.0)', ('pkg', '<', '1.0')),
            ('pkg(>1.0)', ('pkg', '>', '1.0')),
            ('pkg(<=1.0)', ('pkg', '<=', '1.0')),
            ('pkg(>=1.0)', ('pkg', '>=', '1.0')),
            ('pkg(==1.0)', ('pkg', '==', '1.0')),
            ('pkg( <1.0)', ('pkg', '<', '1.0')),
            ('pkg( >1.0)', ('pkg', '>', '1.0')),
            ('pkg( <=1.0)', ('pkg', '<=', '1.0')),
            ('pkg( >=1.0)', ('pkg', '>=', '1.0')),
            ('pkg( ==1.0)', ('pkg', '==', '1.0')),
            ('pkg(<1.0 )', ('pkg', '<', '1.0')),
            ('pkg(>1.0 )', ('pkg', '>', '1.0')),
            ('pkg(<=1.0 )', ('pkg', '<=', '1.0')),
            ('pkg(>=1.0 )', ('pkg', '>=', '1.0')),
            ('pkg(==1.0 )', ('pkg', '==', '1.0')),
            ('pkg( <1.0 )', ('pkg', '<', '1.0')),
            ('pkg( >1.0 )', ('pkg', '>', '1.0')),
            ('pkg( <=1.0 )', ('pkg', '<=', '1.0')),
            ('pkg( >=1.0 )', ('pkg', '>=', '1.0')),
            ('pkg( ==1.0 )', ('pkg', '==', '1.0')),
            ('pkg(<1.0.0)', ('pkg', '<', '1.0.0')),
            ('pkg(>1.0.0)', ('pkg', '>', '1.0.0')),
            ('pkg(<=1.0.0)', ('pkg', '<=', '1.0.0')),
            ('pkg(>=1.0.0)', ('pkg', '>=', '1.0.0')),
            ('pkg(==1.0.0)', ('pkg', '==', '1.0.0')),
            ('pkg( <1.0.0)', ('pkg', '<', '1.0.0')),
            ('pkg( >1.0.0)', ('pkg', '>', '1.0.0')),
            ('pkg( <=1.0.0)', ('pkg', '<=', '1.0.0')),
            ('pkg( >=1.0.0)', ('pkg', '>=', '1.0.0')),
            ('pkg( ==1.0.0)', ('pkg', '==', '1.0.0')),
            ('pkg(<1.0.0 )', ('pkg', '<', '1.0.0')),
            ('pkg(>1.0.0 )', ('pkg', '>', '1.0.0')),
            ('pkg(<=1.0.0 )', ('pkg', '<=', '1.0.0')),
            ('pkg(>=1.0.0 )', ('pkg', '>=', '1.0.0')),
            ('pkg(==1.0.0 )', ('pkg', '==', '1.0.0')),
            ('pkg( <1.0.0 )', ('pkg', '<', '1.0.0')),
            ('pkg( >1.0.0 )', ('pkg', '>', '1.0.0')),
            ('pkg( <=1.0.0 )', ('pkg', '<=', '1.0.0')),
            ('pkg( >=1.0.0 )', ('pkg', '>=', '1.0.0')),
            ('pkg( ==1.0.0 )', ('pkg', '==', '1.0.0')),
            ('pk-g (<1)', ('pk-g', '<', '1')),
            ('pk-g (>1)', ('pk-g', '>', '1')),
            ('pk-g (<=1)', ('pk-g', '<=', '1')),
            ('pk-g (>=1)', ('pk-g', '>=', '1')),
            ('pk-g (==1)', ('pk-g', '==', '1')),
            ('pk-g ( <1)', ('pk-g', '<', '1')),
            ('pk-g ( >1)', ('pk-g', '>', '1')),
            ('pk-g ( <=1)', ('pk-g', '<=', '1')),
            ('pk-g ( >=1)', ('pk-g', '>=', '1')),
            ('pk-g ( ==1)', ('pk-g', '==', '1')),
            ('pk-g (<1 )', ('pk-g', '<', '1')),
            ('pk-g (>1 )', ('pk-g', '>', '1')),
            ('pk-g (<=1 )', ('pk-g', '<=', '1')),
            ('pk-g (>=1 )', ('pk-g', '>=', '1')),
            ('pk-g (==1 )', ('pk-g', '==', '1')),
            ('pk-g ( <1 )', ('pk-g', '<', '1')),
            ('pk-g ( >1 )', ('pk-g', '>', '1')),
            ('pk-g ( <=1 )', ('pk-g', '<=', '1')),
            ('pk-g ( >=1 )', ('pk-g', '>=', '1')),
            ('pk-g ( ==1 )', ('pk-g', '==', '1')),
            ('pk-g (<1.0)', ('pk-g', '<', '1.0')),
            ('pk-g (>1.0)', ('pk-g', '>', '1.0')),
            ('pk-g (<=1.0)', ('pk-g', '<=', '1.0')),
            ('pk-g (>=1.0)', ('pk-g', '>=', '1.0')),
            ('pk-g ( ==1.0)', ('pk-g', '==', '1.0')),
            ('pk-g ( <1.0)', ('pk-g', '<', '1.0')),
            ('pk-g ( >1.0)', ('pk-g', '>', '1.0')),
            ('pk-g ( <=1.0)', ('pk-g', '<=', '1.0')),
            ('pk-g ( >=1.0)', ('pk-g', '>=', '1.0')),
            ('pk-g ( ==1.0)', ('pk-g', '==', '1.0')),
            ('pk-g (<1.0 )', ('pk-g', '<', '1.0')),
            ('pk-g (>1.0 )', ('pk-g', '>', '1.0')),
            ('pk-g (<=1.0 )', ('pk-g', '<=', '1.0')),
            ('pk-g (>=1.0 )', ('pk-g', '>=', '1.0')),
            ('pk-g (==1.0 )', ('pk-g', '==', '1.0')),
            ('pk-g ( <1.0 )', ('pk-g', '<', '1.0')),
            ('pk-g ( >1.0 )', ('pk-g', '>', '1.0')),
            ('pk-g ( <=1.0 )', ('pk-g', '<=', '1.0')),
            ('pk-g ( >=1.0 )', ('pk-g', '>=', '1.0')),
            ('pk-g ( ==1.0 )', ('pk-g', '==', '1.0')),
            ('pk-g (<1.0.0)', ('pk-g', '<', '1.0.0')),
            ('pk-g (>1.0.0)', ('pk-g', '>', '1.0.0')),
            ('pk-g (<=1.0.0)', ('pk-g', '<=', '1.0.0')),
            ('pk-g (>=1.0.0)', ('pk-g', '>=', '1.0.0')),
            ('pk-g (==1.0.0)', ('pk-g', '==', '1.0.0')),
            ('pk-g ( <1.0.0)', ('pk-g', '<', '1.0.0')),
            ('pk-g ( >1.0.0)', ('pk-g', '>', '1.0.0')),
            ('pk-g ( <=1.0.0)', ('pk-g', '<=', '1.0.0')),
            ('pk-g ( >=1.0.0)', ('pk-g', '>=', '1.0.0')),
            ('pk-g ( ==1.0.0)', ('pk-g', '==', '1.0.0')),
            ('pk-g (<1.0.0 )', ('pk-g', '<', '1.0.0')),
            ('pk-g (>1.0.0 )', ('pk-g', '>', '1.0.0')),
            ('pk-g (<=1.0.0 )', ('pk-g', '<=', '1.0.0')),
            ('pk-g (>=1.0.0 )', ('pk-g', '>=', '1.0.0')),
            ('pk-g (==1.0.0 )', ('pk-g', '==', '1.0.0')),
            ('pk-g ( <1.0.0 )', ('pk-g', '<', '1.0.0')),
            ('pk-g ( >1.0.0 )', ('pk-g', '>', '1.0.0')),
            ('pk-g ( <=1.0.0 )', ('pk-g', '<=', '1.0.0')),
            ('pk-g ( >=1.0.0 )', ('pk-g', '>=', '1.0.0')),
            ('pk-g ( ==1.0.0 )', ('pk-g', '==', '1.0.0')),
        ]
        for pkgstr, pkgtpl in depends:
            match = description.re_depends.match(pkgstr)
            self.assertEqual(
                (match.group(1), match.group(3), match.group(4)),
                pkgtpl
            )

    def test_re_pkg_atom(self):
        depends = [
            ('pkg-1', ('pkg', '1')),
            ('pkg-1.0', ('pkg', '1.0')),
            ('pkg-1.0.0', ('pkg', '1.0.0')),
        ]
        for pkgstr, pkgtpl in depends:
            match = description.re_pkg_atom.match(pkgstr)
            self.assertEqual(
                (match.group(1), match.group(2)),
                pkgtpl
            )

    def test_attributes(self):
        # TODO: split this method to improve the error reporting
        # TODO: figure out how to test the comments
        self.assertEqual(self.desc.name, 'package name')
        self.assertEqual(self.desc.version, '0.0.1')
        self.assertEqual(self.desc.date, '2009-01-01')
        self.assertEqual(self.desc.author, 'Author Name: testing \':\'s in the value.')
        self.assertEqual(self.desc.maintainer, 'Maintainer Name')
        self.assertEqual(self.desc.title, 'Package Title')
        self.assertEqual(self.desc.description, 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
        self.assertEqual(self.desc.categories, 'Category1,Category2, Category3')
        self.assertEqual(self.desc.url, 'http://example.org')

        requirements = [
            '>=g-octave/pkg1-4.3.2',
            '<g-octave/pkg2-1.2.3',
            'g-octave/pkg3'
        ]
        self.assertEqual(self.desc.systemrequirements, requirements)
        self.assertEqual(self.desc.buildrequires, ['>g-octave/pkg4-1.0.0'])

        self.assertEqual(self.desc.depends, ['>=sci-mathematics/octave-3.0.0'])
        self.assertEqual(self.desc.autoload, 'NO')
        self.assertEqual(self.desc.license, 'GPL version 3 or later')

    def tearDown(self):
        # removing the temp tree
        utils.clean_env(self._config_file, self._tempdir)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDescription('test_re_depends'))
    suite.addTest(TestDescription('test_re_pkg_atom'))
    suite.addTest(TestDescription('test_attributes'))
    return suite

