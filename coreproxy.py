#!/usr/bin/python
#-*-coding: utf8-*-

import urllib2
import re
import json
import string
import time
import socket

from lxml import etree


class ProxyCrawl():
    '''Crawl proxy'''
    http_proxys = {}

    def __init__(self):
        self.parser = etree.HTMLParser()
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5')]

    def crawl_ipcn(self):
        '''Crawl ipcn find proxy'''
        url = 'http://proxy.ipcn.org/proxylist.html'
        try:
            self.tree = etree.parse(self.opener.open(url, timeout=120), self.parser)
        except socket.timeout:
            return {}
        #self.tree = etree.parse('proxylist.html', self.parser)
        content = self.tree.find('/body/table[@width="100%"]//pre').text
        proxys = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', content)
        proxys = [proxy.split(':') for proxy in proxys]
        http_proxys = {ip: port for ip, port in proxys}
        return http_proxys

    def crawl_proxymore(self):
        '''Crawl proxymore find proxy'''
        url = 'http://www.proxymore.net/proxy_area-CN.html'
        web = self.opener.open(url, timeout=30).read()
        self.tree = etree.fromstring(web, self.parser)
        port = re.search(r'port,\s({.*})', web)
        if port:
            port = re.sub(r'(\w)', "\"\g<1>\"", port.group(1))
            port_map = json.loads(port)
        else:
            raise Exception("No port map")
        trs = self.tree.findall(".//tr[@class='x-tr']")
        http_proxys = {}
        mt = string.maketrans(str(port_map.keys()), str(port_map.values()))
        for proxy in trs:
            ip = proxy.find("./td[@class='pserver']/span").text
            port = proxy.find("./td[@class='pport']/span").text
            port = port.translate(mt)
            http_proxys[ip] = port

        return http_proxys

    def get_proxy(self):
        #self.http_proxys = self.crawl_ipcn()
        self.http_proxys ={}
        self.http_proxys = dict(self.http_proxys, **self.crawl_proxymore())
        http_proxys_list = []
        for ip, port in self.http_proxys.iteritems():
            ipaddr = '%s:%s' % (ip, port)
            http_proxys_list.append(ipaddr)
        return http_proxys_list


class ProxyValidate():
    def __init__(self, test_url='http://www.google.com', timeout=10):
        self.test_url = test_url
        self.timeout = timeout

    def validate(self, proxy):
        '''Validate proxy
           Return 1:OK, 2:TIMEOUT,3:FAILED
        '''
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        befor = time.time()
        try:
            o = opener.open(self.test_url, timeout=self.timeout)
            if o:
                after = time.time()
                elapse = int((after - befor) * 1000)  # ms
                return (1, elapse) if elapse < self.timeout * 1000 else (2, elapse)
            else:
                return (3, 0)
        except Exception:
            return (3, 0)

    def validates(self, proxys):
        '''Validate proxys return (proxy, proxy_status, connect_time)'''
        for proxy in proxys:
            st, time = self.validate(proxy)
            if st == 1:
                yield (proxy, st, time)
            elif st == 2:
                yield (proxy, st, time)
            else:
                continue


if __name__ == '__main__':
    proxy = ProxyCrawl()
    proxys = proxy.get_proxy()
    v = ProxyValidate()
    tcnt = len(proxys)
    print tcnt
    for (a, b, c) in v.validates(proxys):
        print a, b, c
