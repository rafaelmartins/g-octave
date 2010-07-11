# -*- coding: utf-8 -*-

"""
    package_managers.py
    ~~~~~~~~~~~~~~~~~~~

    This module implements some Python classes for the implementation of
    the multiple package manager support.

    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

__all__ = [
    'Portage',
    'Pkgcore',
]

import os
import subprocess


class Base:
    
    _client = ''
    
    post_install = []
    post_uninstall = []
    
    def check_overlay(self, overlay, out):
        return True


class Portage(Base):
    
    _client = 'emerge'
    
    post_uninstall = [
        'You may want to remove the dependencies too, using:',
        '# emerge -av --depclean',
    ]
    
    def __init__(self, ask=False, verbose=False, pretend=False, nocolor=False):
        self._fullcommand = [self._client]
        ask and self._fullcommand.append('--ask')
        verbose and self._fullcommand.append('--verbose')
        pretend and self._fullcommand.append('--pretend')
        nocolor and self._fullcommand.append('--color=n')
    
    def run_command(self, command):
        return subprocess.call(self._fullcommand + command)
    
    def install_package(self, pkgatom):
        return self.run_command([pkgatom])

    def uninstall_package(self, pkgatom):
        return self.run_command(['--unmerge', pkgatom])
    
    def installed_packages(self):
        packages = []
        with open('/var/lib/portage/world') as fp:
            for line in fp:
                if line.startswith('g-octave/'):
                    packages.append(line.strip())
        return packages
    
    def create_manifest(self, ebuild):
        return subprocess.call(['ebuild', ebuild, 'manifest'])
    
    def check_overlay(self, overlay, out):
        import portage
        if overlay not in portage.settings['PORTDIR_OVERLAY'].split(' '):
            out.eerror('g-octave overlay is not configured!')
            out.eerror('You must append your overlay dir to PORTDIR_OVERLAY.')
            out.eerror('Overlay: %s' % overlay)
            return False
        return True


class Pkgcore(Base):
    
    _client = 'pmerge'
    
    post_uninstall = [
        'You may want to remove the dependencies too, using:',
        '# pmerge -av --clean',
    ]
    
    def __init__(self, ask=False, verbose=False, pretend=False, nocolor=False):
        self._fullcommand = [self._client]
        ask and self._fullcommand.append('--ask')
        verbose and self._fullcommand.append('--verbose')
        pretend and self._fullcommand.append('--pretend')
        nocolor and self._fullcommand.append('--nocolor')
    
    def run_command(self, command):
        return subprocess.call(self._fullcommand + command)
    
    def install_package(self, pkgatom):
        return self.run_command([pkgatom])

    def uninstall_package(self, pkgatom):
        return self.run_command(['--unmerge', pkgatom])
    
    def installed_packages(self):
        packages = []
        p = subprocess.Popen([
            'pquery',
            '--vdb',
            '--pkgset=world',
            '--no-version',
            'g-octave/*',
        ], stdout=subprocess.PIPE)
        if p.wait() == os.EX_OK:
            for line in p.stdout:
                packages.append(line.strip())
        return packages
    
    def create_manifest(self, ebuild):
        # from portage :S
        return subprocess.call(['ebuild', ebuild, 'manifest'])
