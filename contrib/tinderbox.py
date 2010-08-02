#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    tinderbox.py
    ~~~~~~~~~~~~
    
    a simple script that tries to build all the packages in the package
    database and report possible build errors.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import os
import portage
import subprocess
import sys
import xmlrpclib

out = portage.output.EOutput()

def g_octave_client():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # try first our local client
    local_client = os.path.realpath(
        os.path.join(current_dir, '..', 'scripts', 'g-octave')
    )
    if os.path.exists(local_client):
        return local_client
    # get it from path
    return 'g-octave'

def sync():
    return subprocess.call([g_octave_client(), '--sync', '--no-colors'])

def list_packages():
    proc = subprocess.Popen([g_octave_client(), '--list-raw'], stdout=subprocess.PIPE)
    if proc.wait() == os.EX_OK:
        return [i.strip() for i in proc.stdout]
    return None

def build_package(atom):
    # forcing portage
    os.environ['GOCTAVE_PACKAGE_MANAGER'] = 'portage'
    return_code = subprocess.call([g_octave_client(), '-v1', '--no-colors', atom])
    build_logs = []
    if return_code != os.EX_OK:
        tmpdir = os.path.join(
            portage.settings['PORTAGE_TMPDIR'],
            'portage',
            'g-octave',
            atom,
            'temp'
        )
        #for f in ['build.log', 'environment']:
        for f in ['build.log']:
            f_ = os.path.join(tmpdir, f)
            if os.path.exists(f_):
                build_logs.append(f_)
    return return_code, build_logs

class TracError(Exception):
    pass

class Trac:
    
    url = 'http://%(user)s:%(passwd)s@www.g-octave.org/trac/login/xmlrpc'
    default_summary = '=g-octave/%(pkgatom)s fails to build. #tinderbox'
    default_description = 'Bug reported by the tinderbox script. See the build logs attached.'
    default_comment = 'Yet another bug report by the tinderbox. More build logs attached: %(filenames)s'
    default_attributes = {
        'type': 'defect',
        'priority': 'major',
        'component': 'ebuilds',
        'keywords': 'tinderbox',
    }
    
    def __init__(self):
        complete_url = self.url % {
            'user': self._get_config('trac_user'),
            'passwd': self._get_config('trac_passwd'),
        }
        self.server = xmlrpclib.ServerProxy(complete_url)
    
    def _get_config(self, key):
        proc = subprocess.Popen([g_octave_client(), '--config', key], stdout=subprocess.PIPE)
        if proc.wait() == os.EX_OK:
            value = proc.stdout.read().strip()
            if value == '':
                value = None
            return value
        return None
    
    def list_tickets(self, pkgatom):
        summary = self.default_summary % {'pkgatom': pkgatom}
        try:
            tickets = self.server.ticket.query('summary=~%s' % summary)
        except xmlrpclib.Fault, exc:
            raise TracError('Failed to list tickets: %s' % exc)
        return tickets
    
    def create_ticket(self, pkgatom):
        summary = self.default_summary % {'pkgatom': pkgatom}
        try:
            ticket_id = self.server.ticket.create(
                summary,
                self.default_description,
                self.default_attributes
            )
        except xmlrpclib.Fault, exc:
            raise TracError('Failed to create the ticket (%s): %s' % (pkgatom, exc))
        return ticket_id
    
    def update_ticket(self, ticket_id, filenames):
        comment = self.default_comment % {'filenames': ', '.join(filenames)}
        try:
            self.server.ticket.update(ticket_id, comment)
        except xmlrpclib.Fault, exc:
            raise TracError('Failed to comment on the ticket (%i): %s' % (ticket_id, exc))
    
    def attach_logs(self, ticket_id, logs):
        filenames = []
        for log in logs:
            with open(log) as fp:
                log_content = xmlrpclib.Binary(fp.read())
            filename = os.path.basename(log)
            try:
                filenames.append(self.server.ticket.putAttachment(
                    ticket_id,
                    filename,
                    filename,
                    log_content,
                    False
                ))
            except xmlrpclib.Fault, exc:
                raise TracError('Failed to upload the attachment (%s): %s' % (log, exc))
        return filenames

def main(argv):
    out.einfo('Starting the tinderbox ...')
    try:
        trac = Trac()
        failures = []
        sync()
        packages = list_packages()
        for package in packages:
            out.einfo('Building the package: %s' % package)
            return_code, logs = build_package(package)
            if return_code != os.EX_OK:
                failures.append(package)
                out.eerror('Build failed!!! Sending the logs ...')
                # error found, look at the logs
                tickets = trac.list_tickets(package)
                if len(tickets) == 0:
                    # create a new ticket
                    out.einfo('Creating a new ticket ...')
                    ticket_id = trac.create_ticket(package)
                else:
                    # will update the oldest soon
                    out.einfo('Found an old ticket for this package, will send a comment.')
                    ticket_id = tickets[0]
                out.einfo('Attaching the logs ...')
                filenames = trac.attach_logs(ticket_id, logs)
                if len(tickets) > 0:
                    out.einfo('Filling a comment in the ticket ...')
                    trac.update_ticket(ticket_id, filenames)
                out.einfo('Bug report done.')
            else:
                out.einfo('OK!')
    except TracError, exc:
        print >> sys.stderr, exc
        return os.EX_SOFTWARE
    else:
        if len(failures) > 0:
            out.eerror('Failures: %s' % ', '.join(failures))
        return os.EX_OK

if __name__ == '__main__':
    sys.exit(main(sys.argv))
