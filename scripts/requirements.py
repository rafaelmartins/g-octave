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
import portage

from _emerge.actions import load_emerge_config
from _emerge.search import search

current_dir = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(current_dir, '..', 'g_octave')):
    sys.path.insert(0, os.path.join(current_dir, '..'))

from g_octave import description, description_tree, exception

def main(argv):

    if len(argv) <= 1:
        print >> sys.stderr, 'one argument required: the json file.'
        return 1

    # init portage stuff
    settings, trees, mtimedb = load_emerge_config()
    root_config = trees[settings['ROOT']]['root_config']
    s = search(root_config, False, False, False, False, False)

    desc_tree = description_tree.DescriptionTree(parse_sysreq = False)

    # identifier => list of dependencies
    dependencies = dict()

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
                my_dep = match.group(1)
                my_match = my_dep.split('-')[0]
                if my_match not in dependencies:
                    dependencies[my_match] = [my_dep]
                else:
                    dependencies[my_match].append(my_dep)

    json_dict = dict(dependencies=dict())

    try:
        with open(argv[1], 'r') as fp:
            json_dict = json.load(fp)
    except:
        pass

    for dep in dependencies:
        s.execute(dep)
        print dep
        temp = []
        for i in range(len(s.matches['pkg'])):
            print '    %i: %s' % (i, s.matches['pkg'][i][0])
            temp.append(s.matches['pkg'][i][0])

        if dependencies[dep][0] in json_dict['dependencies']:
            select = raw_input('Select a package [%s]: ' % \
                json_dict['dependencies'][dependencies[dep][0]])
        else:
            select = raw_input('Select a package: ')
        try:
            for dep_name in dependencies[dep]:
                json_dict['dependencies'][dep_name] = temp[int(select)]
        except:
            if select != '' or dependencies[dep][0] not in json_dict['dependencies']:
                for dep_name in dependencies[dep]:
                    json_dict['dependencies'][dep_name] = select
        print 'Selected: %s' % json_dict['dependencies'][dependencies[dep][0]]
        print

    try:
        with open(argv[1], 'w') as fp:
            json.dump(json_dict, fp, sort_keys=True, indent=4)
    except:
        print >> sys.stderr, 'failed to save the json file.'
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
