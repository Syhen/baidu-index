# -*- coding: utf-8 -*-
"""
create on 2018-10-07 下午1:10

author @heyao
"""
from collections import OrderedDict

from baidu_index.api.index import API_INDEX_HOST

API_HOST = 'https://passport.baidu.com'

API_INDEX_HOME = {
    'host': API_INDEX_HOST,
    'path': '/',
    'mark': '?',
    'method': 'GET',
    'query': {
        'tpl': 'trend',
        'word': '{query}'
    }
}
API_PRE_TOKEN = {
    'host': 'https://passport.baidu.com/static/passpc-base/js/ld.min.js?cdnversion=1538893906660',
    'path': '',
    'method': 'GET',
    'mark': '',
    'query': {}
}

API_GET_TOKEN = {
    'host': API_HOST,
    'path': '/v2/api/?getapi',
    'method': 'GET',
    'mark': '&',
    'query': OrderedDict([
        (u'tpl', u'mn'), (u'apiver', u'v3'), (u'tt', u'{tt}'), (u'class', u'login'), (u'gid', u'{gid}'),
        (u'loginversion', u'v4'), (u'logintype', u'dialogLogin'), (u'traceid', u''),
        (u'callback', u'bd__cbs__{callback}'),
    ])
}

API_GET_KEYS = {
    'host': API_HOST,
    'path': '/v2/getpublickey',
    'method': 'GET',
    'mark': '?',
    'query': {
        'token': '{token}',
        'tpl': 'mn',
        'apiver': 'v4',
        'tt': '{tt}',
        'gid': '{gid}',
        'callback': 'bd__cbs__{callback}'
    }
}
