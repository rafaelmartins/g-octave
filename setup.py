#!/usr/bin/env python

import warnings
warnings.filterwarnings('ignore')

from distutils.core import setup
import g_octave

setup(
    name='g-octave',
    version = g_octave.__version__,
    license = g_octave.__license__,
    description = g_octave.__description__,
    long_description = open('README.rst').read(),
    author = g_octave.__author__,
    author_email = g_octave.__email__,
    url = g_octave.__url__,
    packages = ['g_octave'],
    scripts = ['scripts/g-octave'],
    data_files = [('/etc', ['etc/g-octave.cfg'])],
    requires = ['portage']
)
