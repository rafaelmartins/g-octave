#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Config']

import ConfigParser
import json
import os

from exception import ConfigException

class Config(object):
    
    __defaults = {
        'db': '/var/cache/g-octave',
        'overlay': '/usr/local/portage/g-octave',
        'categories': 'main,extra,language',
        'db_mirror': 'http://files.rafaelmartins.eng.br/octave-forge',
    }

    __section_name = 'main'


    def __init__(self, fetch_phase=False):
        
        # Config Parser
        self.__config = ConfigParser.ConfigParser(self.__defaults)
        
        if os.path.exists('../etc/g-octave.cfg.devel'):
            self.__config_file = '../etc/g-octave.cfg.devel'
        else:
            self.__config_file = '/etc/g-octave.cfg'
        
        self.__config.read(self.__config_file)
        
        __db = self.__config.get(self.__section_name, 'db')
        __overlay = self.__config.get(self.__section_name, 'overlay')
        
        for dir in [__db, __overlay]:
            if not os.path.exists(dir):
                os.makedirs(dir, 0755)
        
        if not fetch_phase:
            
            # Cache (JSON)
            cache_file = os.path.join(__db, 'cache.json')
            fp = open(cache_file)
            self.__cache = json.load(fp)
            fp.close()
            
            # JSON
            json_file = os.path.join(__db, self.__cache['files']['info.json'])
            fp = open(json_file)
            self.__info = json.load(fp)
            fp.close()
        

    def __getattr__(self, attr):
        
        if self.__defaults.has_key(attr):
            return self.__config.get(self.__section_name, attr)
        elif self.__info.has_key(attr):
            return self.__info[attr]
        elif attr == 'cache':
            return self.__cache['files']
        else:
            raise ConfigException('Invalid option: %s' % attr)
