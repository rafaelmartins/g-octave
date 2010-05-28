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

from g_octave import config, overlay


class TestOverlay(unittest.TestCase):
    
    def setUp(self):
        self._config_file = tempfile.mkstemp(suffix='.cfg')[1]
        self._dir = tempfile.mkdtemp()
        
        # the directories doesn't need to be created. the config module
        # will do this
        self._db = os.path.join(self._dir, 'db')
        self._cache = os.path.join(self._dir, 'cache')
        self._overlay = os.path.join(self._dir, 'overlay')
        
        cp = ConfigParser.ConfigParser()
        cp.add_section('main')
        cp.set('main', 'db', self._db)
        cp.set('main', 'cache', self._cache)
        cp.set('main', 'overlay', self._overlay)
        
        with open(self._config_file, 'w') as fp:
            cp.write(fp)
        
        self._config = config.Config(
            fetch_phase = True,
            config_file = self._config_file,
            create_dirs = True
        )

    def test_overlay(self):
        overlay.create_overlay(conf = self._config, quiet = True) 

    def tearDown(self):
        shutil.rmtree(self._dir)
        os.unlink(self._config_file)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestOverlay('test_overlay'))
    return suite
        
