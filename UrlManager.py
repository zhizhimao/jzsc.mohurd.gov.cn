#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 11:41:45 2018
@author: 星空飘飘
编辑器：Spyder
开发环境：Anaconda 3-5.1.0
Python 3.6.4

URL管理器： UrlManager.py
"""


class UrlManager(object):
    def __init__(self):
        self.new_urls = set()  # 未爬取的URL集合
        self.old_urls = set()  # 已爬取的URL集合

    def has_new_url(self):
        '''判断是否还有未爬取的URL'''
        return self.new_url_size() != 0

    def get_new_url(self):
        '''获取一个未爬取的URL'''
        if self.has_new_url() is True:
            new_url = self.new_urls.pop()  # 取出一个URL并删除
            self.old_urls.add(new_url)  # 添加一个URL到已爬取集合
            return new_url
        else:
            print('已经没有可以获取的URL链接!')

    def add_new_url(self, url):
        '''将新的URL添加到未爬取的URL集合中'''
        if url is None:  # url是否空
            return
        # 是否在未爬取集合，是否在已爬取集合，如果都不在就添加到未爬取集合中
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''将新的URL添加到未爬取的URL集合中'''
        # 新增的URL集合是否是空或是0
        if urls is None or len(urls) == 0:
            return
        for url in urls:  # 将URL添加到未爬取集合
            self.add_new_url(url)

    def new_url_size(self):
        '''获取未爬取的URL集合大小'''
        return len(self.new_urls)

    def old_url_size(self):
        '''获取已爬取URL集合大小'''
        return len(self.old_urls)


'''
import json

with open('urls.json', 'r', encoding='utf-8') as f:
    urls = json.load(f)
urls_list = [i for i in urls.values()][0]

debug = UrlManager()
debug.add_new_urls(urls_list)

# 判断是否还有未爬取的URL
debug.has_new_url()

# 获取一个未爬取的URL
debug.get_new_url()

# 获取已爬取URL集合大小
debug.old_url_size()

# 获取未爬取的URL集合大小
debug.new_url_size()
'''
