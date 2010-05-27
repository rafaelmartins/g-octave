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
import tempfile
import unittest

from g_octave import description, description_tree


class TestDescriptionTree(unittest.TestCase):
    
    _packages = [
        ('main', 'pkg1', '1.0'),
        ('main', 'pkg2', '0.1'),
        ('main', 'pkg2', '0.2'),
        ('extra', 'pkg1', '1.1'),
        ('language', 'lang', '0.1'),
    ]
       
    def setUp(self):
        description_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'DESCRIPTION'
        )
        
        # creating a temporary DESCRIPTION's tree
        self._tree_dir = tempfile.mkdtemp()
        for cat, pkg, ver in self._packages:
            temp_path = os.path.join(self._tree_dir, cat, pkg+'-'+ver)
            os.makedirs(temp_path)
            shutil.copy(
                description_file,
                os.path.join(temp_path, 'DESCRIPTION')
            )
        self._tree = description_tree.DescriptionTree(self._tree_dir)
    
    def test_temptree(self):
        for cat, pkg, ver in self._packages:
            temp_file = os.path.join(
                self._tree_dir,
                cat, pkg+'-'+ver,
                'DESCRIPTION'
            )
            self.assertTrue(os.path.exists(temp_file))
    
    def test_package_versions(self):
        versions = {
            'pkg1': ['1.0', '1.1'],
            'pkg2': ['0.1', '0.2'],
            'lang': ['0.1'],
        }
        for pkg in versions:
            ver = self._tree.package_versions(pkg)
            ver.sort()
            versions[pkg].sort()
            self.assertEqual(versions[pkg], ver)
    
    def test_latest_version(self):
        versions = {
            'pkg1': '1.1',
            'pkg2': '0.2',
            'lang': '0.1',
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
        for cat, pkg, ver in self._packages:
            self.assertTrue(
                isinstance(
                    self._tree[pkg+'-'+ver],
                    description.Description
                )
            ) 
    
    def tearDown(self):
        # removing the temp tree
        shutil.rmtree(self._tree_dir)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDescriptionTree('test_temptree'))
    suite.addTest(TestDescriptionTree('test_package_versions'))
    suite.addTest(TestDescriptionTree('test_latest_version'))
    suite.addTest(TestDescriptionTree('test_version_compare'))
    suite.addTest(TestDescriptionTree('test_description_files'))
    return suite
