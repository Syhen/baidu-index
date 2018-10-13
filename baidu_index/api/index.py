# -*- coding: utf-8 -*-
"""
create on 2018-10-10 上午11:30

author @heyao
"""
API_INDEX_HOST = "http://index.baidu.com"
API_INDEX_ENCRYPT_INDEXES = {
    "host": API_INDEX_HOST,
    "path": "/Interface/Search/getSubIndex/",
    "mark": "?",
    "method": "GET",
    "query": {
        "res": "{res}",
        "res2": "{res2}",
        "type": "0",
        "startdate": "{start_date}",
        "enddate": "{end_date}",
        "forecast": "0",
        "word": "{query}"
    }
}

API_INDEX_DECRYPT_INDEXES = {
    'host': API_INDEX_HOST,
    'path': '/Interface/IndexShow/show/',
    'mark': '?',
    'method': 'GET',
    'query': {
        'res': '{res}',
        'res2': '{res2}',
        'classType': '1',
        'res3[]': '{encrypt_index}',
        'className': 'view-value'
    },
    'avoid_cache': True
}
