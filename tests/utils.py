#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~
    
    module with helper functions to the test suites.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import shutil
import tempfile

def create_description_tree(packages):
    # 'packages' is a list of tuples, like this:
    # [(category, name, version)]
    description_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'DESCRIPTION'
    )
    
    # creating a temporary DESCRIPTION's tree
    tree_dir = tempfile.mkdtemp()
    for cat, pkg, ver in packages:
        temp_path = os.path.join(tree_dir, cat, pkg+'-'+ver)
        os.makedirs(temp_path)
        shutil.copy(
            description_file,
            os.path.join(temp_path, 'DESCRIPTION')
        )
    return tree_dir
