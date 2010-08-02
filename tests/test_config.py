#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_config.py
    ~~~~~~~~~~~~~~
    
    test suite for the *g_octave.config* module
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import unittest

from g_octave import config


class TestConfig(unittest.TestCase):
    
    def setUp(self):
        # TODO: fetch_phase = False
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # object with the config file empty, should use the default values
        self._empty_cfg = config.Config(
            config_file = os.path.join(current_dir, 'files', 'g-octave_empty.cfg'),
            create_dirs = False,
            fetch_phase = True
        )
        
        # object with an example config file
        self._cfg = config.Config(
            config_file = os.path.join(current_dir, 'files', 'g-octave.cfg'),
            create_dirs = False,
            fetch_phase = True
        )
    
    def test_empty_config_attributes(self):
        self.assertEqual(self._empty_cfg.db, '/var/cache/g-octave')
        self.assertEqual(self._empty_cfg.overlay, '/var/lib/g-octave')
        self.assertEqual(self._empty_cfg.categories, 'main,extra,language')
        self.assertEqual(self._empty_cfg.db_mirror, 'github://rafaelmartins/g-octave-db')
        self.assertEqual(self._empty_cfg.trac_user, '')
        self.assertEqual(self._empty_cfg.trac_passwd, '')
        self.assertEqual(self._empty_cfg.log_level, '')
        self.assertEqual(self._empty_cfg.log_file, '/var/log/g-octave.log')
        self.assertEqual(self._empty_cfg.package_manager, 'portage')
    
    def test_config_attributes(self):
        self.assertEqual(self._cfg.db, '/path/to/the/db')
        self.assertEqual(self._cfg.overlay, '/path/to/the/overlay')
        self.assertEqual(self._cfg.categories, 'comma,separated,categories,names')
        self.assertEqual(self._cfg.db_mirror, 'http://some.cool.url/octave-forge/')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConfig('test_empty_config_attributes'))
    suite.addTest(TestConfig('test_config_attributes'))
    return suite
