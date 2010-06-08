#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    requirements.py
    ~~~~~~~~~~~~~~~
    
    a simple script that creates a JSON file with the list of dependencies
    that are not from octave-forge package (SystemRequirements and
    BuildRequires). It writes the JSON content to the stdout.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import json
import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(current_dir, '..', 'g_octave')):
    sys.path.insert(0, os.path.join(current_dir, '..'))

from g_octave import description, description_tree, exception

def main(argv):
    desc_tree = description_tree.DescriptionTree(parse_sysreq = False)
    
    dependencies = []
    
    for pkg in desc_tree.packages():
        try:
            desc = desc_tree[pkg]
        except exception.DescriptionTreeException, err:
            print >> sys.stderr, 'DescriptionTree error: %s' % err
            return 1
        
        deps = []
        
        if desc.systemrequirements is not None:
            deps += [i.strip() for i in desc.systemrequirements.split(',')]
        
        if desc.buildrequires is not None:
            deps += [i.strip() for i in desc.buildrequires.split(',')]
        
        for dep in deps:
            match = description.re_depends.match(dep)
            if match is not None:
                dependencies.append(match.group(1))
    
    json_dict = dict(dependencies=dict())
    
    for dep in dependencies:
        json_dict['dependencies'][dep] = ''
    
    json.dump(json_dict, sys.stdout, sort_keys=True, indent=4)
    
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
