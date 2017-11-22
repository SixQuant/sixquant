# coding=utf-8

import socket
import time

import requests

from ..utils.logger import logger

_USER_AGENTS = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Chrome/57.0.2987.133',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Safari/537.36',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
]


def url_get_host(url):
    """
    从URL中找出 HOST 部分
    get_host('http[s]://host[:port]/path') --> 'host'.
    :param url:
    :return:
    """
    if url is None or url == '':
        return None

    pos = url.find('://')
    if -1 != pos:
        url = url[pos + 3:]

    pos1 = url.find(':')
    if -1 == pos1:
        pos1 = len(url)

    pos2 = url.find('/')
    if -1 == pos2:
        pos2 = len(url)

    if pos2 < pos1:
        pos1 = pos2

    host = url[: pos1]
    return host


class Fetcher(object):
    """
    抓取器
    """

    def __init__(self):
        pass

    # ==========================================================================================

    def http_response_handle(self, target, status, content):
        """
        留给子类进行重载
        比如访问被拒绝等常规检查用
        :param target:
        :param status:
        :param content:
        :return:
        """
        return status, content

    def http_request_impl(self, method, target, headers, data, charset, timeout, callback):
        """
        留给子类进行重载
        最终抓取功能实现，这里用了 requests 库
        :param method:
        :param target:
        :param headers:
        :param data:
        :param charset:
        :param timeout:
        :param callback:
        :return:
        """

        headers = self.http_prepare_headers(target, headers)

        if data is None:
            data = {}

        if method.upper() == 'GET':
            r = requests.get(target, headers=headers, data=data, timeout=timeout)
        else:
            r = requests.post(target, headers=headers, data=data, timeout=timeout)

        if charset is not None:
            r.encoding = charset
        return r.status_code, r.text

    # ==========================================================================================

    def rnd(self):
        return str(int(time.time() * 1000))

    def get_next_user_agent(self):
        """
        更换 user-agent 有利于反抓取
        :return:
        """

        return 'Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)'

    # ==========================================================================================

    def http_prepare_headers(self, target, headers=None):
        """补全请求字段"""
        if headers is None:
            headers = {}

        if 'Host' not in headers:
            headers['Host'] = url_get_host(target)

        if 'User-Agent' not in headers:
            headers['User-Agent'] = self.get_next_user_agent()

        return headers

    def http_request(self,
                     method,
                     target,
                     headers=None,
                     data=None,
                     charset=None,
                     timeout=60,
                     retry_times=9,
                     retry_sleep_factor=5000,
                     callback=None
                     ):
        """
        带重试功能的 http request
        :param method:
        :param target:
        :param headers:
        :param data:
        :param charset:
        :param timeout:
        :param retry_times:
        :param retry_sleep_factor:
        :param callback:
        :return:
        """
        # 超时重试
        retried = -1
        while True:
            retried = retried + 1
            try:
                status, content = self.http_request_impl(method, target, headers, data, charset, timeout, callback)
                break
            except (socket.gaierror, socket.timeout, requests.exceptions.ConnectTimeout) as e:
                if retried > 0:
                    log = logger.get(__name__)
                    log.warning("Warning: %s socket timeout. retried %d times." % (target, retried))
                if retried > retry_times:
                    raise e
                time.sleep(retry_sleep_factor * (retried + 1) * 0.001)

        if status not in (200, 201, 456):
            log = logger.get(__name__)
            log.warning(content)

        return self.http_response_handle(target, status, content)

    # ==========================================================================================

    def http_get_js(self, target,
                    headers=None,
                    data=None,
                    charset=None,
                    timeout=60,
                    retry_times=9,
                    retry_sleep_factor=5000,
                    callback=None):
        if headers is None:
            headers = {'Content-type': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Cache-Control': 'max-age=0',
                       'Connection': 'keep-alive',
                       'Accept-Language': 'en-US,en;q=0.5'
                       }
        return self.http_request('GET',
                                 target,
                                 headers=headers,
                                 data=data,
                                 charset=charset,
                                 timeout=timeout,
                                 retry_times=retry_times,
                                 retry_sleep_factor=retry_sleep_factor,
                                 callback=callback
                                 )

    def http_get_html(self, target,
                      headers=None,
                      data=None,
                      charset=None,
                      timeout=60,
                      retry_times=9,
                      retry_sleep_factor=5000,
                      callback=None):
        if headers is None:
            headers = {'Content-type': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Cache-Control': 'max-age=0',
                       'Connection': 'keep-alive',
                       'Accept-Language': 'en-US,en;q=0.5'
                       }
        return self.http_request('GET',
                                 target,
                                 headers=headers,
                                 data=data,
                                 charset=charset,
                                 timeout=timeout,
                                 retry_times=retry_times,
                                 retry_sleep_factor=retry_sleep_factor,
                                 callback=callback
                                 )

    def http_get_json(self, target,
                      headers=None,
                      data=None,
                      charset=None,
                      timeout=60,
                      retry_times=9,
                      retry_sleep_factor=5000,
                      callback=None):
        if headers is None:
            headers = {'Content-type': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Cache-Control': 'max-age=0',
                       'Connection': 'keep-alive',
                       'Accept-Language': 'en-US,en;q=0.5'
                       }
        return self.http_request('GET',
                                 target,
                                 headers=headers,
                                 data=data,
                                 charset=charset,
                                 timeout=timeout,
                                 retry_times=retry_times,
                                 retry_sleep_factor=retry_sleep_factor,
                                 callback=callback
                                 )

    def http_post_json(self, target,
                       headers=None,
                       data=None,
                       charset=None,
                       timeout=60,
                       retry_times=9,
                       retry_sleep_factor=5000,
                       callback=None):
        if headers is None:
            headers = {'Content-type': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Cache-Control': 'max-age=0',
                       'Connection': 'keep-alive',
                       'Accept-Language': 'en-US,en;q=0.5'
                       }
        return self.http_request('POST',
                                 target,
                                 headers=headers,
                                 data=data,
                                 charset=charset,
                                 timeout=timeout,
                                 retry_times=retry_times,
                                 retry_sleep_factor=retry_sleep_factor,
                                 callback=callback
                                 )

    def http_get_text(self, target,
                      headers=None,
                      data=None,
                      charset=None,
                      timeout=60,
                      retry_times=9,
                      retry_sleep_factor=5000,
                      callback=None):
        if headers is None:
            headers = {'Content-type': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate',
                       'Cache-Control': 'max-age=0',
                       'Connection': 'keep-alive',
                       'Accept-Language': 'en-US,en;q=0.5'
                       }
        return self.http_request('GET',
                                 target,
                                 headers=headers,
                                 data=data,
                                 charset=charset,
                                 timeout=timeout,
                                 retry_times=retry_times,
                                 retry_sleep_factor=retry_sleep_factor,
                                 callback=callback
                                 )


fetcher = Fetcher()
