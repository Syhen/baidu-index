# -*- coding: utf-8 -*-
"""
create on 2018-10-07 下午5:16

author @heyao
"""
from baidu_index.api.parameters import API_HOST

API_LOGIN_JS = {
    'host': 'https://ss0.bdstatic.com',
    'path': '/5LMZfyabBhJ3otebn9fN2DJv/passApi/js/loginv4_b66a29e.js',
    'mark': '',
    'method': 'GET',
    'query': {}
}
API_HOME = {
    'host': 'http://www.baidu.com',
    'path': '/',
    'mark': '',
    'method': 'GET',
    'query': {}
}

API_LOGIN_CHECK = {
    'host': API_HOST,
    'path': '/v2/api/?logincheck',
    'method': 'GET',
    'mark': '&',
    'query': {
        'token': '{token}',
        'tpl': 'mn',
        'apiver': 'v3',
        'tt': '{tt}',
        'sub_source': 'leadsetpwd',
        'username': '{username}',
        'loginversion': 'v4',
        'dv': '',
        'traceid': '',
        'callback': 'bd__cbs__{callback}'
    }
}

API_LOGIN_HISTORY = {
    'host': API_HOST,
    'path': '/v2/api/?loginhistory',
    'method': 'GET',
    'mark': '&',
    'query': {
        'token': '{token}',
        'tpl': 'mn',
        'apiver': 'v3',
        'tt': '{tt}',
        'loginversion': 'v4',
        'gid': '{gid}',
        'traceid': '',
        'callback': 'bd__cbs__{callback}'
    }
}

API_REGGET_CODESTR = {
    'host': API_HOST,
    'path': '/v2/?reggetcodestr',
    'method': 'GET',
    'mark': '&',
    'query': {
        'token': '{token}',
        'tpl': 'mn',
        'apiver': 'v3',
        'tt': '{tt}',
        'fr': 'login',
        'loginversion': 'v4',
        'vcodetype': '{vcodetype}',
        'traceid': '',
        'callback': 'bd__cbs__{callback}'
    }
}

API_GET_VERIFY_IMG = {
    'host': API_HOST,
    'path': '/cgi-bin/genimage',
    'method': 'GET',
    'mark': '?',
    'query': {
        '': '{codestr}'
    }
}

API_CHECH_VERIFY_CODE = {
    'host': API_HOST,
    'path': '/v2/?checkvcode',
    'method': 'GET',
    'mark': '&',
    'query': {
        'token': '{token}',
        'tpl': 'mn',
        'apiver': 'v3',
        'tt': '{tt}',
        'verifycode': '{verify_code}',
        'loginversion': 'v4',
        'codestring': '{codestr}',
        'traceid': '',
        'callback': 'bd__cbs__{callback}'
    }
}

API_LOGIN = {
    'host': API_HOST,
    'path': '/v2/api/?login',
    'method': 'POST',
    'mark': '',
    'post_data': {
        "staticpage": "https%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fv3Jump.html",
        "charset": "UTF-8",
        "token": "{token}",
        "tpl": "mn",
        "subpro": "",
        "apiver": "v3",
        "tt": "{tt}",
        "codestring": "",
        "safeflg": "0",
        "u": "https%3A%2F%2Fwww.baidu.com%2F",
        "isPhone": "false",
        "detect": "1",
        "gid": "{gid}",
        "quick_user": "0",
        "logintype": "dialogLogin",
        "logLoginType": "pc_loginDialog",
        "idc": "",
        "loginmerge": "true",
        "splogin": "rate",
        "username": "{username}",
        "password": "{password}",
        # "verifycode": "",
        "mem_pass": "on",
        "traceid": "",
        "loginversion": "v4",
        "fp_uid": "",
        "fp_info": "",
        "rsakey": "{rsakey}",
        "crypttype": "12",
        "ppui_logintime": "6825",
        "countrycode": "",
        "callback": "parent.bd__pcbs__{callback}"
    }
}
