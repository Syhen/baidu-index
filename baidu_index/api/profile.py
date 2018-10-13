# -*- coding: utf-8 -*-
"""
create on 2018-10-13 上午2:17

author @heyao
"""
from baidu_index.api.index import API_INDEX_HOST

API_INDEX_DECRYPT_INDEXES = {
    'host': API_INDEX_HOST,
    'path': '/Interface/Region/getRegion/',
    'mark': '?',
    'method': 'GET',
    'query': {
        'res': '{res}',
        'res2': '{res2}',
        'region': '0'
    }
}
