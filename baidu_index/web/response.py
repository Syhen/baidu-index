# -*- coding: utf-8 -*-
"""
create on 2018-10-07 下午1:43

author @heyao
"""
import time

import requests
from copy import deepcopy

from baidu_index.login.encode import urlencode


def _fill_data(data, **kwargs):
    """根据{key}填充
    :param data: dict. 需要填充的数据
    :param kwargs: `data` 中的所有key，都必需有该参数传入
    :return: dict. 填充完的数据
    """
    for key in data:
        val = data[key]
        if '{' in val:
            k = val[val.index('{') + 1: val.index('}')]
            data[key] = val.format(**{k: kwargs[k]})
    return data


def make_response(api, cookies=None, headers=None, **kwargs):
    """根据api字典，生成 `requests.Response`
    :param api: dict. 请求的api数据结构
    :param cookies: `requests.cookies.RequestsCookieJar`. request的cookie 
    :param headers: dict. 请求头
    :param kwargs: dict. api中需要填充的数据
    :return: `requests.Response`
    """
    local_api = deepcopy(api)
    method = local_api['method']
    headers = headers or {}
    if method == 'GET':
        query = local_api['query']
        query = _fill_data(query, **kwargs)
        url = local_api['host'] + local_api['path'] + local_api['mark'] + urlencode(query)
        data = None
        if local_api.get('avoid_cache', False):
            url += '&' + str(int(time.time()))
    elif method == "POST":
        url = local_api['host'] + local_api['path']
        data = local_api['post_data']
        data = _fill_data(data, **kwargs)
        data = urlencode(data)
    else:
        raise ValueError("method must be 'GET' or 'POST', got %s" % method)
    response = requests.request(method, url, cookies=cookies, headers=headers, data=data)
    return response


if __name__ == '__main__':
    from baidu_index.api.parameters import API_GET_TOKEN, API_PRE_TOKEN
    from baidu_index.login.parameters import get_tt, get_callback, random_guid

    response = make_response(API_PRE_TOKEN)
    response = make_response(API_GET_TOKEN, cookies=response.cookies, tt=get_tt(), gid=random_guid(),
                             callback=get_callback())
    print response.content
