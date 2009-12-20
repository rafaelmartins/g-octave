#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    'Config',
    'ConfigException',
]

import ConfigParser
import simplejson
import portage
import os

class ConfigException(Exception):
    pass


class Config(object):
    
    __defaults = {
        'db': '/var/cache/octave-forge',
        'overlay': portage.settings['PORTDIR'] + '/local/g-octave',
        'categories': 'main,extra,language',
        'db_mirror': 'http://files.rafaelmartins.eng.br/octave-forge',
    }

    __section_name = 'main'


    def __init__(self):
        
        # Config Parser
        self.__config = ConfigParser.ConfigParser(self.__defaults)
        
        if os.path.exists('/etc/g-octave.cfg'):
            self.__config_file = '/etc/g-octave.cfg'
        else:
            self.__config_file = '../etc/g-octave.cfg.devel'
        
        self.__config.read(self.__config_file)
    
        # JSON
        fp = open(os.path.join(self.__getattr__('db'), 'info.json'))
        self.__info = simplejson.load(fp)
        fp.close()
        

    def __getattr__(self, attr):
        
        if self.__defaults.has_key(attr):
            return self.__config.get(self.__section_name, attr)
        elif self.__info.has_key(attr):
            return self.__info[attr]
        else:
            raise ConfigException('Invalid option: %s' % attr)
        

if __name__ == '__main__':
    conf = Config()
    print conf.dependencies, conf.blacklist
