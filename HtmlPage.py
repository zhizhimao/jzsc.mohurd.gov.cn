#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 13:15:32 2018

@author: 星空飘飘

编辑器：Spyder
开发环境：Anaconda 3-5.1.0
Python 3.6.4

HTML解析器: Html_Page.py
"""

import re
from lxml import etree
import pandas as pd


class HtmlPage(object):
    def get_specified_search_urls(self, html):
        '''解析指定企业名称搜索数据'''
        if html:
            page = etree.HTML(html)
        try:
            # 企业名称
            enterprise_name = page.xpath('/html/body/div/div/table/tbody/tr/td/a/em/text()')
            if len(enterprise_name) == 1:
                enterprise_name = str(enterprise_name[0])
            else:
                print('“搜索输入企业名称全称！”')
            # 企业编码 用于创建新链接的数字编码
            enterprise_num = str(page.xpath('/html/body/div/div/table/tbody/tr/td[3]/a/@href')[0])  # 找到所有的a标记
            num = re.findall('(\d+)', enterprise_num)[0]
            # 企业资质资格
            cadetail = f'http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/{num}'
            # 注册人员
            regstaff = f'http://jzsc.mohurd.gov.cn/dataservice/query/comp/regStaffList/{num}'
            # 工程项目
            compperformance = f'http://jzsc.mohurd.gov.cn/dataservice/query/comp/compPerformanceListSys/{num}'
            urls = [cadetail, regstaff, compperformance]  # 构建urls
            # 构造字典类型数据
            urls_list = {enterprise_name: urls}
            return urls_list
        except Exception as e:
            print('获取内容失败!')

    def get_search_urls(self, html):
        '''解析根据条件搜索数据如企业资质、注册地'''
        if html:
            page = etree.HTML(html)
        try:
            # 企业名称
            enterprise_name = []
            en_list = page.xpath('/html/body/div/div/table/tbody/tr/td[3]/a/text()')
            for i in en_list:
                en = re.findall('\S+', i)
                enterprise_name.extend(en)
            # 企业编码 用于创建新链接的数字编码
            enterprise_coding = []
            ec_list = page.xpath('/html/body/div/div/table/tbody/tr/td/a')  # 找到所有的a标记
            for i in ec_list:
                num = re.findall('\d+', (i.xpath('./@href')[0]))
                num = num[0]
                # 企业资质资格
                cadetail = f'http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/{num}'
                # 注册人员
                regstaff = f'http://jzsc.mohurd.gov.cn/dataservice/query/comp/regStaffList/{num}'
                # 工程项目
                compperformance = f'http://jzsc.mohurd.gov.cn/dataservice/query/comp/compPerformanceListSys/{num}'
                urls = [cadetail, regstaff, compperformance]  # 构建urls
                enterprise_coding.append(urls)
            # 构造字典类型数据
            urls = dict(zip(enterprise_name, enterprise_coding))
            return urls
        except Exception as e:
            print('获取内容失败!')

    def get_total_pg(self, html):
        '''获取总的页数和总条数'''
        try:
            pc = re.findall('<div class="clearfix">.*?pc:(\d+).*?</a>', html)  # 页数
            tt = re.findall('<div class="clearfix">.*?tt:(\d+).*?</a>', html)  # 条数
            return pc, tt
        except Exception as error:
            return None

    def get_enterprise_qualifications(self, name, html):
        '''企业资质'''
        try:
            cadetaillist = re.findall('td data-header=.*? style="text-align:.*?">\s+(.*?)\s+</td>', html, re.S)
            df = pd.DataFrame([[name], cadetaillist])
            df = df.T
            df.rename(columns={0: '企业名称', 1: '企业资质'}, inplace=True)
            df['企业名称'] = df['企业名称'].fillna(name)  # None替换名称
            return df
        except Exception as error:
            return None

    def get_registrar(self, name, html):
        '''注册人员'''
        try:
            # 所有注册人员数
            reg_num = dict(re.findall('<a class="formsubmit " .*?">(.*?)<span>.(\d+).</span></a>', html, re.S))  # 生产字典类型
            df = pd.DataFrame(reg_num, index=[0], dtype='float')  # 转换pandas数据框架
            df = df.T
            df.reset_index(inplace=True)
            df['企业名称'] = pd.DataFrame([name])
            df.rename(columns={'index': '注册证', 0: '注册人员'}, inplace=True)
            df['企业名称'] = df['企业名称'].fillna(name)  # None替换名称
            return df
        except Exception as error:
            return None

    def get_Enterprise_performance(self, name, html):
        '''企业业绩'''
        # 项目名称
        projectname = re.findall('<td data-header="项目名称" style="text-align:left;"><a href="javascript:;" onclick="top.window.location.href=.*?">(.*?)</a></td>', html, re.S)
        # 项目编号
        projectnum = re.findall('<td data-header="项目编码">(.*?)</td>',html,re.S)
        projectlink = []
        for num in projectnum:
            link = f'http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/{num}'
            projectlink.append(link)
        # 项目属地
        territoriality = re.findall('<td data-header="项目属地">(.*?)</td>', html, re.S)
        # 项目类别
        category = re.findall('<td data-header="项目类别">(.*?)</td>', html, re.S)
        # 建设单位
        build = re.findall('<td data-header="建设单位" style="text-align:left;">(.*?)</td>', html, re.S)
        # 构造字典类型数据
        data = pd.DataFrame([[name], projectname, projectlink, territoriality, category, build])
        df = data.T
        df.rename(columns={0: '企业名称', 1: '项目名称', 2: '项目链接', 3: '项目属地', 4: '项目类别', 5:  '建设单位'}, inplace=True)
        df['企业名称'] = df['企业名称'].fillna(name)  # None替换名称
        return df


'''
debug = HtmlPage()
# 解析指定企业名称搜索获取urls
urls = debug.get_specified_search_urls(html)

# 解析根据条件搜索数据如企业资质、注册地
urls = debug.get_search_urls(html)
# 获取总的页数和总条数
pc, tt = debug.get_total_pg(html)

# 企业资质
name = '中恒工程设计院有限公司'
df = debug.get_enterprise_qualifications(name, html)

# 注册人员
name = '中恒工程设计院有限公司'
df = debug.get_registrar(name, html)

# 企业业绩
df = debug.get_Enterprise_performance(name, html)
'''
