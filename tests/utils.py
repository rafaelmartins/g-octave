#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    utils.py
    ~~~~~~~~
    
    module with helper functions to the test suites.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import ConfigParser
import os
import shutil
import tempfile

from g_octave import config

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

def create_env():
    """returns a tuple with the *g_octave.config* object and the path of
    the temporary config and directory
    """
    
    config_file = tempfile.mkstemp(suffix='.cfg')[1]
    directory = tempfile.mkdtemp()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(current_dir, 'files')
    overlay = os.path.join(directory, 'overlay')
    
    cp = ConfigParser.ConfigParser()
    cp.add_section('main')
    cp.set('main', 'db', db)
    cp.set('main', 'overlay', overlay)
    
    with open(config_file, 'w') as fp:
        cp.write(fp)
    
    conf = config.Config(
        fetch_phase = True,
        config_file = config_file,
        create_dirs = True
    )
    
    return conf, config_file, directory
    
def clean_env(config_file, directory):
    os.unlink(config_file)
    shutil.rmtree(directory)
