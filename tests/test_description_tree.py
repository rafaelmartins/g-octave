#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    test_description_tree.py
    ~~~~~~~~~~~~~~~~~~~~~~~~
    
    test suite for the *g_octave.description_tree* module
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import shutil
import unittest
import utils

from g_octave import description, description_tree


class TestDescriptionTree(unittest.TestCase):
    
    def setUp(self):
        conf, self._config_file, self._tempdir = utils.create_env()
        self._tree = description_tree.DescriptionTree(conf = conf)
    
    def test_package_versions(self):
        versions = {
            'main1': ['0.0.1'],
            'main2': ['0.0.1', '0.0.2'],
            'extra1': ['0.0.1'],
            'extra2': ['0.0.1', '0.0.2'],
            'language1': ['0.0.1'],
            'language2': ['0.0.1', '0.0.2'],
        }
        for pkg in versions:
            ver = self._tree.package_versions(pkg)
            ver.sort()
            versions[pkg].sort()
            self.assertEqual(versions[pkg], ver)
    
    def test_latest_version(self):
        versions = {
            'main1': '0.0.1',
            'main2': '0.0.2',
            'extra1': '0.0.1',
            'extra2': '0.0.2',
            'language1': '0.0.1',
            'language2': '0.0.2',
        }
        for pkg in versions:
            self.assertEqual(
                versions[pkg],
                self._tree.latest_version(pkg)
            )
    
    def test_version_compare(self):
        # TODO: cover a better range of versions
        versions = [
            # ((version1, version2), latest_version)
            (('1', '2'), '2'),
            (('0.1', '1'), '1'),
            (('0.1', '0.2'), '0.2'),
            (('0.0.1', '1'), '1'),
            (('0.0.1', '0.1'), '0.1'),
            (('0.0.1', '0.0.2'), '0.0.2'),
            (('2', '1'), '2'),
            (('1', '0.1'), '1'),
            (('0.2', '0.1'), '0.2'),
            (('1', '0.0.1'), '1'),
            (('0.1', '0.0.1'), '0.1'),
            (('0.0.2', '0.0.1'), '0.0.2'),
        ]
        for ver, latest in versions:
            self.assertEqual(self._tree.version_compare(ver), latest)
    
    def test_description_files(self):
        packages = [
            ('main', 'main1', '0.0.1'),
            ('main', 'main2', '0.0.1'),
            ('main', 'main2', '0.0.2'),
            ('extra', 'extra1', '0.0.1'),
            ('extra', 'extra2', '0.0.1'),
            ('extra', 'extra2', '0.0.2'),
            ('language', 'language1', '0.0.1'),
            ('language', 'language2', '0.0.1'),
            ('language', 'language2', '0.0.2'),
        ]
        for cat, pkg, ver in packages:
            self.assertTrue(
                isinstance(
                    self._tree[pkg+'-'+ver],
                    description.Description
                )
            ) 
    
    def tearDown(self):
        # removing the temp tree
        utils.clean_env(self._config_file, self._tempdir)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDescriptionTree('test_package_versions'))
    suite.addTest(TestDescriptionTree('test_latest_version'))
    suite.addTest(TestDescriptionTree('test_version_compare'))
    suite.addTest(TestDescriptionTree('test_description_files'))
    return suite
