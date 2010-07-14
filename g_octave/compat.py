# -*- coding: utf-8 -*-

"""
    compat.py
    ~~~~~~~~~
    
    This module implements some helper function to compatibility with
    Python 3k.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

__all__ = [
    'py3k',
    'open_py3k',
]

import codecs
import sys

py3k = sys.version_info >= (3, 0)

#open = py3k and open or codecs.open

def open_py3k(filename, mode, **kwargs):
    if 'encoding' not in kwargs:
        kwargs['encoding'] = 'utf-8'
    if py3k:
        return open(filename, mode, **kwargs)
    return codecs.open(filename, mode, **kwargs)
