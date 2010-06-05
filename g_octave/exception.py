# -*- coding: utf-8 -*-

"""
    exception.py
    ~~~~~~~~~~~~
    
    This module implements some Python classes that are the exceptions
    raised by g-Octave.
    
    :copyright: (c) 2009-2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

__all__ = [
    'ConfigException',
    'DescriptionException',
    'DescriptionTreeException',
    'EbuildException',
    'FetchException',
]


class ConfigException(Exception):
    pass

class DescriptionException(Exception):
    pass

class DescriptionTreeException(Exception):
    pass

class EbuildException(Exception):
    pass

class FetchException(Exception):
    pass
