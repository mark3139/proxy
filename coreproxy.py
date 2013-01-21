#!/usr/bin/python
#-*-coding: utf8-*-

import urllib2
import re

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
        self.http_proxys = {ip: port for ip, port in proxys}

if __name__ == '__main__':
    p = ProxyCrawl()
    p.crawl_ipcn()
