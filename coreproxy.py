#!/usr/bin/python
#-*-coding: utf8-*-

import urllib2
import re
import json
import string
import time

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
        #self.tree = etree.parse(self.opener.open(url), self.parser)
        self.tree = etree.parse('proxylist.html', self.parser)
        content = self.tree.find('/body/table[@width="100%"]//pre').text
        proxys = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', content)
        proxys = [proxy.split(':') for proxy in proxys]
        http_proxys = {ip: port for ip, port in proxys}
        return http_proxys

    def crawl_proxymore(self):
        '''Crawl proxymore find proxy'''
        url = 'http://www.proxymore.net/proxy_area-CN.html'
        #web = self.opener.open(url)
        #self.tree = etree.parse(web, self.parser)
        web = file('proxy_area-CN.html')
        self.tree = etree.parse('proxy_area-CN.html', self.parser)
        port = re.search(r'\(port,\s({.*})', web.read())
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
        self.http_proxys = self.crawl_ipcn()
        self.http_proxys = dict(self.http_proxys, **self.crawl_proxymore())


class Proxy():
    def __init__(self, proxys):
        self.test_url = 'http://www.baidu.com'

    def validate(self, proxy):
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        befor = time.time()
        try:
            o = opener.open(self.test_url)
            if o:
                after = time.time()
                return (1, int((after - befor) * 1000))
            else:
                return (0, 0)
        except Exception:
            return (0, 0)

if __name__ == '__main__':
    p = Proxy('')
    print p.validate('119.254.90.18:8080')
