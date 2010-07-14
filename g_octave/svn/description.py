# -*- coding: utf-8 -*-

"""
    description.py
    ~~~~~~~~~~~~~~

    This module implements a wrapper to the g_octave.description module,
    creating a description object from the SVN trunk DESCRIPTION file of
    a package.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import tempfile

from g_octave.svn import client
from g_octave import description, exception

class SvnDescription(description.Description):
    
    def __init__(self, category, package):
        self._svn = client.SvnClient(create_revisions=False)
        temp_desc = config_file = tempfile.mkstemp()[1]
        try:
            self._svn.download_file(
                category + '/' + package + '/DESCRIPTION',
                temp_desc
            )
        except:
            raise exception.DescriptionException('Failed to fetch DESCRIPTION file from SVN')
        description.Description.__init__(self, temp_desc, parse_sysreq=True)
        os.unlink(temp_desc)
