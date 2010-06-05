#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    trac.py
    ~~~~~~~
    
    A Python module to interact with a Trac instance.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import csv
import pycurl
import re
import sys
import StringIO
import urllib

class TracError(Exception):
    pass

class Trac(object):
    
    url = 'http://g-octave.rafaelmartins.eng.br/'
    
    def __init__(self, user, passwd):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.COOKIEFILE, '/tmp/curl_cookie.txt')
        self.curl.setopt(pycurl.COOKIEJAR, '/tmp/curl_cookie.txt')
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.user = user
        self.token, autenticated = self._get_token()
        if not autenticated:
            code, html = self.request(
                self.url + 'login', [
                    ('user', user),
                    ('password', passwd),
                    ('__FORM_TOKEN', self.token),
                ]
            )
            if code != 200 or not self.user_autenticated(html):
                raise TracError('Autentication failed!')
        
    
    def user_autenticated(self, html):
        return html.find('<a href="/logout">') != -1

    
    def _get_token(self):
        code, html = self.request(self.url + 'query')
        match = re.search(r'__FORM_TOKEN"[^>]+value="([^"]+)"', html)
        if match != None:
            return match.group(1), self.user_autenticated(html)
        else:
            raise TracError('Failed to parse FORM_TOKEN.')
        
    
    def create_ticket(self, summary, description):
        code, html = self.request(
            self.url + 'newticket', [
                ('__FORM_TOKEN', self.token),
                ('field_component', 'ebuilds'),
                ('field_priority', 'minor'),
                ('field_reporter', self.user),
                ('field_type', 'defect'),
                ('field_summary', summary),
                ('field_description', description),
                ('field_owner', 'rafaelmartins'),
            ]
        )
        match = re.search(r'#([0-9]+) \(%s\)' % summary, html)
        if code != 200 or match is None:
            raise TracError('Failed to create a new ticket.')
        return int(match.group(1))
    
    
    def attach_file(self, id, description, filename):
        code, html = self.request(
            self.url + 'attachment/ticket/' + str(id) + '/', [
                ('attachment', (pycurl.FORM_FILE, filename)),
                ('__FORM_TOKEN', self.token),
                ('id', str(id)),
                ('action', 'new'),
                ('realm', 'ticket'),
                ('description', description),
            ],
            upload = True
        )
        if code != 200:
            raise TracError('Failed to send the attachment.')
        match = re.search(r'"/attachment/ticket/%i/([^"]+)"' % int(id), html)
        if match is None:
            raise TracError('Failed to find the attachment link.')
        return match.group(1)
    
    
    def list_tickets(self, summary):
        params = [
            ('format', 'csv'),
            ('component', 'ebuilds'),
            ('summary', '~' + summary),
            ('col', [
                'id',
                'summary',
                'status',
            ])
        ]
        results = []
        code, html = self.request(
            self.url + 'query?' + urllib.urlencode(params, True),
        )
        if code != 200:
            sys.exit('Failed to request the list of tickets.')
        fp = csv.reader(StringIO.StringIO(html))
        result = list(fp)
        keys = result[0]
        for i in range(1, len(result)):
            tmp = {}
            for j in range(len(keys)):
                tmp[keys[j]] = result[i][j]
            results.append(tmp)
        return results

    
    def request(self, url, params=None, upload=False):
        self.curl.setopt(pycurl.URL, url)
        if params is not None:
            self.curl.setopt(pycurl.POST, 1)
            self.curl.setopt(pycurl.HTTPPOST, params)
        if upload:
            self.curl.setopt(pycurl.HTTPHEADER, ['Expect:'])
        buffer = StringIO.StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        try:
            self.curl.perform()
        except pycurl.error, err:
            raise TracError('HTTP request failed: %s' % err)
        return self.curl.getinfo(pycurl.HTTP_CODE), buffer.getvalue()


