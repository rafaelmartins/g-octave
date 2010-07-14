# -*- coding: utf-8 -*-

"""
    log.py
    ~~~~~~
    
    a simple Python module to deal with g-octave logging stuff.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

from __future__ import print_function, absolute_import

import logging
import sys

from .config import Config
conf = Config(fetch_phase=True)


class Log(object):
    
    _levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(self.name)
        has_file = conf.log_file is not None and conf.log_file != ''
        has_level = conf.log_level is not None and conf.log_level != ''
        if not has_file:
            print('WARNING: no "log_file" configured. logging disabled.', file=sys.stderr)
        if not has_file or not has_level:
            class NullHandler(logging.Handler):
                def emit(self, record):
                    pass
            self.handler = NullHandler()
        else:
            self.handler = logging.FileHandler(conf.log_file)
        self.level = self._levels.get(conf.log_level, logging.NOTSET)
        self.logger.setLevel(self.level)
        self.handler.setLevel(self.level)
        self.formatter = \
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
    
    def __getattr__(self, attr):
        if attr in ['debug', 'info', 'warning', 'error', 'critical']:
            return getattr(self.logger, attr)
        return lambda x: None
