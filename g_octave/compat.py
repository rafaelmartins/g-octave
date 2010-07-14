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
    'open',
]

import codecs
import sys

py3k = sys.version_info >= (3, 0)

def open(filename, mode='r', encoding='utf-8'):
    try:
        return codecs.open(filename, mode=mode, encoding=encoding)
    except:
        return codecs.open(filename, mode=mode, encoding='iso-8859-15')
