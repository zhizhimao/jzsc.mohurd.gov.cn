#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:52:27 2018

@author: 星空飘飘

编辑器：Spyder
开发环境：Anaconda 3-5.1.0
Python 3.6.4
数据存储: SaveData.py

保存url json格式
保存企业资质 csv格式
保存注册人员 csv格式
保存企业业绩 csv格式
"""
import json


class SaveData(object):
    def save_urls(self, urls):
        '''保存urls到文件中,name保存文件名,urls是数据'''
        with open('urls.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(urls, indent=4, ensure_ascii=False))  # indent 格式化保存字典，默认为None，小于0为零个空格; ensure_ascii=False 输出中文

    def save_cadetail(self, df):
        df.to_csv('企业资质.csv', mode='a', index=0, encoding='utf-8')

    def save_regstaff(self, df):
        df.to_csv('注册人员.csv', mode='a', index=0, encoding='utf-8')

    def save_compperformance(self, df):
        df.to_csv('企业业绩.csv', mode='a', index=0, encoding='utf-8')


'''
debug = SaveData()

# 保存urls
debug.save_urls(urls)

# 保存企业资质
debug.save_cadetail(df)

# 保存注册人员
debug.save_regstaff(df)

# 保存企业业绩
debug.save_compperformance(df)
'''
