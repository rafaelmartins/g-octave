#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_ebuild.py
    ~~~~~~~~~~~~~~
    
    test suite for the *g_octave.ebuild* module
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import unittest
import utils

from g_octave import ebuild


class TestEbuild(unittest.TestCase):
    
    def setUp(self):
        self._config, self._config_file, self._dir = utils.create_env()
    
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
    
    def tearDown(self):
        utils.clean_env(self._config_file, self._dir)
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEbuild('test_re_keywords'))
    return suite
