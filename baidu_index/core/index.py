# -*- coding: utf-8 -*-
"""
create on 2018-10-09 下午3:19

author @heyao
"""
from __future__ import unicode_literals

import base64
import json
from StringIO import StringIO

import re
from datetime import datetime
from urllib import quote

import requests
from PIL import Image
from lxml import etree

from baidu_index import api
from baidu_index.core.recognizer import recognize_baidu_index
from baidu_index.web.response import make_response

RE_RES = re.compile(r"PPval\.ppt = \'(.*?)\',")
RE_RES2_CODES = re.compile(r'<script type="text/javascript">\nT\(([\s\S]*)</script>')
RE_RES2_VAR = re.compile(r"BID\.res2\((\w+)\);")
RE_RES2 = re.compile(r'<span id="baidu-index">(.*?)</span>')
RE_IMG_URL = re.compile(r'url\("(.*?)"\)')
lua_code_format = """function main(splash)
    assert(splash:go("%s"))
    while not splash:evaljs("document.readyState === 'complete'") do
        splash:wait(0.05)
    end
    return {html=splash:html(), url=splash:url()}
end"""


def get_res(content):
    """获取res
    根据正则提取res
    :param content: str. 百度指数首页的html   
    :return: str.
    """
    return RE_RES.findall(content)[0]


def get_res2_logistic_codes(content):
    """获取计算res2的逻辑代码
    :param content: str. 百度指数首页的html 
    :return: str.
    """
    not_in_start = {
        '}', ']', 'BID.', 'T(', 'if', 'var', 'this.href', 'var word',
        '<script', '$', '<', 'function', 'snapshot', '//', 'document',
        'pop', 'bdShare', 'return', 'setTimeout', 'for', 'opts', '"', '.',
        '#', 'trendChartInit'
    }
    not_in_line = {':'}
    javascript = RE_RES2_CODES.findall(content)[0]
    js_codes = []
    for line in javascript.split('\n'):
        line = line.strip()
        if not line:
            continue
        if any(i in line for i in not_in_line) or any(line.startswith(i) for i in not_in_start):
            continue
        js_codes.append(line)
    res2_var = RE_RES2_VAR.findall(javascript)[0]
    js_codes.append('document.getElementById("baidu-index").innerHTML = %s;' % res2_var)
    return js_codes


def get_res2(logistic_codes):
    """获取res2
    :param logistic_codes: list. 计算res2的js逻辑代码 
    :return: str.
    """
    js_code_str = base64.b64encode(json.dumps(logistic_codes))
    url_get = 'http://192.168.1.5/baidu/res2?js_code=%s' % js_code_str
    lua_code = lua_code_format % url_get
    url = 'http://localhost:8050/execute?lua_source=%s' % quote(lua_code)
    response = requests.get(url)
    return RE_RES2.findall(response.json()['html'])[0]


def splice_img(img, widths, positions):
    """拼接百度图片
    根据图片、每个crop的宽度，每个crop的位置拼接指数图片
    :param img: `PIL.Image`. 拼接原始图片
    :param widths: list. 每个分片的宽度
    :param positions: list. 每个分片的大小
    :return: `PIL.Image`. 拼接好之后的图片
    """
    w, h = img.size
    total_width = sum(widths)
    target = Image.new("1", size=(total_width, h))
    iwidth = 0
    for width, position in zip(widths, positions):
        im = img.crop(((-position % w), 0, (-position % w) + width, h))
        target.paste(im, (iwidth, 0, iwidth + width, h))
        im.close()
        iwidth += width
    return target


def parse_style_code(code, cookies):
    """解析指数数据样式代码
    :param code: str. 指数数据样式代码
    :param cookies: `requests.cookies.RequestsCookieJar`. request的cookie，用于获取待拼接图片
    :return: list, list, bytes 宽度、位置、图片数据
    """
    sel = etree.HTML(code)
    widths = [int(i[6: -3]) for i in sel.xpath('//span[@class="imgval"]/@style')]
    positions = [int(i[12: -3]) for i in sel.xpath('//div[@class="imgtxt"]/@style')]
    img_data = None
    while not img_data:
        img_url = api.API_INDEX_HOST + RE_IMG_URL.findall(code)[0]
        img_data = requests.get(img_url, cookies=cookies).content
    return widths, positions, img_data


def parse_index_img(img_data, widths, positions):
    """解析指数图片数据
    :param img_data: bytes. 图片数据
    :param widths: list. 每个分片的宽度
    :param positions: list. 每个分片的大小 
    :return: str. 识别后的指数数据
    """
    with Image.open(StringIO(img_data)) as img:
        total_img = splice_img(img, widths, positions)
    return ''.join(recognize_baidu_index(total_img))


class BaiduIndexCrawler(object):
    """百度指数爬虫"""

    def __init__(self, query, cookies, start_date=None, end_date=None, platform='all'):
        """
        :param query: str. 查询关键词，不能含有逗号 
        :param cookies: `requests.cookie.RequestCookieJar` 或 dict. 登录后的cookie
        :param start_date: str. 数据开始时间
        :param end_date: str. 数据结束时间
        :param platform: str. all, pc, wise
        """
        if any(i in query for i in (',', '，')):
            raise ValueError("query must not have ',' or '，'")
        self.query_word = query
        self.query = quote(query.encode('gb2312'))
        self.cookies = cookies
        if (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).total_seconds() < 0:
            raise ValueError("end_date must greater than or equal start_date")
        self.start_date = start_date
        self.end_date = end_date
        self.platform = platform
        self.encrypt_indexes = []
        self.indexes = []
        self.cursor = 0
        self.res = None
        self.res2 = None
        self._finished = False
        self.init_params()

    def init_params(self):
        """初始化参数
        初始化res, res2参数
        """
        response = make_response(api.API_INDEX_HOME, cookies=self.cookies, query=self.query)
        self.cookies.update(response.cookies)
        content = response.content.decode('gbk', 'ignore').replace('\r\n', '\n')
        res = get_res(content)
        res2 = get_res2(get_res2_logistic_codes(content))
        self.res = res
        self.res2 = res2

    def get_encrypt_indexes(self):
        """获取加密后的指数"""
        response = make_response(api.API_INDEX_ENCRYPT_INDEXES, cookies=self.cookies, res=self.res, res2=self.res2,
                                 start_date=self.start_date, end_date=self.end_date, query=quote(str(self.query_word)))
        self.cookies.update(response.cookies)
        indexes = response.json()['data']
        self.encrypt_indexes = indexes[self.platform][0]['userIndexes_enc'].split(',')
        return indexes

    def fetch_index(self, encrypt_index):
        """根据加密后的指数，获取加密前的指数
        :param encrypt_index: str. 加密后的指数
        :return: int. 加密前的指数
        """
        response = make_response(api.API_INDEX_DECRYPT_INDEXES, cookies=self.cookies, res=self.res, res2=self.res2,
                                 encrypt_index=encrypt_index)
        self.cookies.update(response.cookies)
        index_code = response.json()['data']['code'][0]
        widths, positions, img_data = parse_style_code(index_code, self.cookies)
        index = int(parse_index_img(img_data, widths, positions).replace(',', ''))
        return index

    def next(self):
        if self.cursor < len(self.encrypt_indexes):
            encrypt_index = self.encrypt_indexes[self.cursor]
            index = self.fetch_index(encrypt_index)
            self.indexes.append(index)
            self.cursor += 1
            return index
        self._finished = True
        raise StopIteration()

    def __iter__(self):
        return self


if __name__ == '__main__':
    import os
    import sys

    from requests.cookies import RequestsCookieJar

    reload(sys)
    sys.setdefaultencoding('utf8')

    cookie_str = os.environ.get("BAIDU_COOKIE")
    cookies = RequestsCookieJar()
    for cookie in cookie_str.split(';'):
        key, val = cookie.strip().split('=', 1)
        cookies[key] = val
    baidu_index_crawler = BaiduIndexCrawler(u'比特币', cookies, start_date="2017-01-01", end_date="2017-01-31")
    baidu_index_crawler.get_encrypt_indexes()
    for index in baidu_index_crawler:
        print index
