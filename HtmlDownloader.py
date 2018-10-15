#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建时间：Sun Oct 14 16:00:37 2018
作者: 星空飘飘
平台：Anaconda 3-5.1.0
语言版本：Python 3.6.4
编辑器：Spyder 3.2.6
分析器：Pandas: 0.22.0
解析器：lxml: 4.1.1
数据库：MongoDB 2.6.12
程序名：HtmlDownloader.py
"""
import requests


class HtmlDownloader(object):
    '''下载网页内容'''
    def __init__(self):
        self.headers = {'Host': 'jzsc.mohurd.gov.cn',
                        'Origin': 'http://jzsc.mohurd.gov.cn',
                        'Referer': 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
                        }

    def get_html(self, url='http://jzsc.mohurd.gov.cn/dataservice/query/comp/list', pg=None, apt_code=None, qy_name=None, region=None, qy_type='QY_ZZ_ZZZD_004'):
        '''获取企业数据信息'''
        data = {'apt_code': apt_code,   # 资质名称代码 ( A1A )
                'qy_fr_name': '',  # 企业法人代表
                '$total': '',  # 总的企业数
                'qy_reg_addr': '',  # 企业注册属地
                'qy_code': '',     # 统一社会信用代码
                'qy_name': qy_name,    # 企业名称
                'qy_region': region,  # 企业注册属地编码510000四川
                'qy_type': qy_type,  # 资质类别 QY_ZZ_ZZZD_004设计企业
                '$pg': pg,    # 打开页
                'qy_gljg': '',     # 造价企业所属管理机构  510000 四川
                'apt_scope': '',  # 资质名称 工程设计综合资质甲级
                'complexname': ''  # 条件筛选
                }  # 构建发送数据
        try:
            # 网站内容禁止跳转allow_redirects=False
            response = requests.post(url=url, data=data, headers=self.headers, allow_redirects=False, timeout=2)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                html = response.text
                return html
            else:
                return pg
        except Exception as error:
            return None


'''
debug = HtmlDownloader()
html = debug.get_html(qy_name='中国市政工程西南设计研究总院有限公司', pg=1, region='510000')

# 企业资质
url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/001607220057383548'
html = debug.get_html(url,pg=1)

# 注册人员
url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/regStaffList/001607220057383548'
html = debug.get_html(url,pg=1)

# 企业业绩
url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/compPerformanceListSys/001607220057383548'
html = debug.get_html(url,pg=1)

# 项目详细信息
url = 'http://jzsc.mohurd.gov.cn/dataservice/query/project/projectDetail/3205841709190201'
html = debug.get_html(url)
'''
