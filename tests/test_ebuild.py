#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_ebuild.py
    ~~~~~~~~~~~~~~
    
    test suite for the *g_octave.ebuild* module
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import unittest
import utils

from g_octave import ebuild, overlay


class TestEbuild(unittest.TestCase):
    
    def setUp(self):
        self._config, self._config_file, self._dir = utils.create_env(json_files=True)
        overlay.create_overlay(conf = self._config, quiet = True)
    
    def test_re_keywords(self):
        keywords = [
            ('alpha', (None, 'alpha')),
            ('amd64', (None, 'amd64')),
            ('hppa', (None, 'hppa')),
            ('ppc', (None, 'ppc')),
            ('ppc64', (None, 'ppc64')),
            ('sparc', (None, 'sparc')),
            ('x86', (None, 'x86')),
            ('~alpha', ('~', 'alpha')),
            ('~amd64', ('~', 'amd64')),
            ('~hppa', ('~', 'hppa')),
            ('~ppc', ('~', 'ppc')),
            ('~ppc64', ('~', 'ppc64')),
            ('~sparc', ('~', 'sparc')),
            ('~x86', ('~', 'x86')),
        ]
        
        for kwstr, kwtpl in keywords:
            match = ebuild.re_keywords.match(kwstr)
            self.assertEqual(
                (match.group(1), match.group(2)),
                kwtpl
            )
    
    def test_generated_ebuilds(self):
        ebuilds = [
            ('main1', '0.0.1'),
            ('main2', '0.0.1'),
            ('extra1', '0.0.1'),
            ('extra2', '0.0.1'),
            ('language1', '0.0.1'),
            ('language2', '0.0.1'),
        ]
        for pkgname, pkgver in ebuilds:
            _ebuild = ebuild.Ebuild(
                pkgname + '-' + pkgver,
                conf = self._config,
            )
            _ebuild.create(
                accept_keywords = 'amd64 ~amd64 x86 ~x86',
                manifest = False,
                display_info = False
            )
            created_ebuild_file = os.path.join(
                self._config.overlay,
                'g-octave', pkgname,
                pkgname + '-' + pkgver + '.ebuild'
            )
            original_ebuild_file = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'files', 'ebuilds',
                pkgname + '-' + pkgver + '.ebuild'
            )
            
            # compare ebuilds, line by line
            with open(created_ebuild_file) as fp:
                created_ebuild = fp.readlines()
            with open(original_ebuild_file) as fp:
                original_ebuild = fp.readlines()
            self.assertEqual(len(created_ebuild), len(original_ebuild))
            for i in range(len(created_ebuild)):
                self.assertEqual(created_ebuild[i], original_ebuild[i])            
    
    def tearDown(self):
        utils.clean_env(self._config_file, self._dir)
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEbuild('test_re_keywords'))
    suite.addTest(TestEbuild('test_generated_ebuilds'))
    return suite
