#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
