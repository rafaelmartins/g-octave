#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    trac.py
    ~~~~~~~
    
    a Python module to interact with a Trac instance.
    
    :copyright: (c) 2010 by Rafael Goncalves Martins
    :license: GPL-2, see LICENSE for more details.
"""

import cookielib
import csv
import re
import sys
import urllib
import urllib2


class Trac(object):
    
    url = 'http://g-octave.rafaelmartins.eng.br/'
    
    def __init__(self, user, passwd):
        self.user = user
        cj = cookielib.FileCookieJar('cookie.txt')
        cj.load('cookie.txt')
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.token = self._get_token()
        params = {
            'user': user,
            'password': passwd,
            '__FORM_TOKEN': self.token,
        }
        try:
            fp = self.opener.open(self.url + 'login', urllib.urlencode(params))
            html = fp.read()
        except:
            sys.exit('Failed to send authentication data.')
        else:
            if re.search(r'Invalid username or password', html) is not None:
                sys.exit('Invalid username or password.')

    
    def _get_token(self):
        try:
            fp = self.opener.open(self.url + 'login')
            html = fp.read()
        except:
            sys.exit('Failed to get FORM_TOKEN.')
        else:
            match = re.search(r'__FORM_TOKEN"[^>]+value="([^"]+)"', html)
            if match != None:
                return match.group(1)
            else:
                sys.exit('Failed to parse FORM_TOKEN.')
    
    
    def create_ticket(self, summary, description):
        params = {
            '__FORM_TOKEN': self.token,
            'field_component': 'ebuilds',
            'field_priority': 'minor',
            'field_reporter': self.user,
            'field_type': 'defect',
            'field_summary': summary,
            'field_description': description,
            'field_owner': 'rafaelmartins', # hardcoded :(
        }
        try:
            fp = self.opener.open(self.url + 'newticket', urllib.urlencode(params))
            html = fp.read()
        except:
            sys.exit('Failed to send ticket data.')
        else:
            match = re.search(r'#([0-9]+) \(%s\)' % summary, html)
            if match is not None:
                return int(match.group(1))
    
    
    def attach_file(self, id, description, file):
        params = {
            '__FORM_TOKEN': self.token,
            'id': id,
            'action': 'new',
            'realm': 'ticket',
            'description': description,
            'attachment': open(file, 'rb')
        }
        try:
            req = urllib2.Request(
                self.url + 'attachment/ticket/' + str(id) + '/',
                urllib.urlencode(params), {}
            )
            fp = self.opener.open(req)
            html = fp.read()
        except:
            sys.exit('Failed to send attachment data.')
        else:
            print html
            #match = re.search(r'#([0-9]+) \(%s\)' % summary, html)
            #if match is not None:
            #    return int(match.group(1))
        finally:
            fp.close()
    
    
    def list_tickets(self, pkgatom):
        params = [
            ('format', 'csv'),
            ('component', 'ebuilds'),
            ('summary', '~' + pkgatom),
            ('col', [
                'id',
                'summary',
                'status',
            ])
        ]
        results = []
        try:
            fp = csv.reader(self.opener.open(self.url + 'query?' + 
                urllib.urlencode(params, True)))
            result = list(fp)
            keys = result[0]
            for i in range(1, len(result)):
                tmp = {}
                for j in range(len(keys)):
                    tmp[keys[j]] = result[i][j]
                results.append(tmp)
            return results
        except:
            sys.exit('Failed to get the ticket list.')


