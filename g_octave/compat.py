# -*- coding: utf-8 -*-

"""
    compat.py
    ~~~~~~~~~
    
    This module implements some compatibility helpers.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

__all__ = [
    'open',
]

import codecs

def open(filename, mode='r', encoding='utf-8'):
    try:
        return codecs.open(filename, mode=mode, encoding=encoding)
    except:
        return codecs.open(filename, mode=mode, encoding='iso-8859-15')
