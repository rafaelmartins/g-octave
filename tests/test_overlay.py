#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_overlay.py
    ~~~~~~~~~~~~~~~
    
    test suite for the *g_octave.overlay* module
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import ConfigParser
import os
import shutil
import tempfile
import unittest
import utils

from g_octave import config, overlay


class TestOverlay(unittest.TestCase):
    
    def setUp(self):
        self._config, self._config_file, self._dir = utils.create_env()

    def test_overlay(self):
        overlay.create_overlay(conf = self._config, quiet = True)
        files = {
            os.path.join(self._config.overlay, 'eclass', 'octave-forge.eclass'): '',
            os.path.join(self._config.overlay, 'profiles', 'repo_name'): 'g-octave',
            os.path.join(self._config.overlay, 'profiles', 'categories'): 'g-octave',
        }
        for _file in files:
            self.assertTrue(os.path.exists(_file))
            with open(_file) as fp:
                self.assertEqual(fp.read(), files[_file])

    def tearDown(self):
        utils.clean_env(self._config_file, self._dir)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestOverlay('test_overlay'))
    return suite
        
