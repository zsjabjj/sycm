# -*- coding: utf-8 -*-
import json
import logging

import scrapy

from Sycm.pipelines import MideaPipeline
from Sycm.settings import custom_settings_for_midea, _CATEID, _INDEXS
from utils.DateRangeAndTimeStamp import date_range, time_stamp


class MideaSpider(scrapy.Spider):

    print('midea')

    pipeline = {MideaPipeline, }
    custom_settings = custom_settings_for_midea

    name = 'midea'
    allowed_domains = ['sycm.taobao.com']
    # start_urls = ['http://midea.com/']

    # 时间范围 4。8--6。30

    start_time, end_time, dateType, index = date_range()
    dateRange = start_time + '%7C' + end_time
    print(dateRange)
    # dateRange = ''
    # _time = ''

    # 行业大盘
    # dapanUrl = 'https://sycm.taobao.com/mq/overview/reportTrend.json?cateId=50004390&dateRange=2018-07-15%7C2018-07-15&dateType=recent1&device=0&indexCode=uv|searchUvCnt|payPct|payItemQty&seller=-1&token=9a0425930&_=1531711927828'
    dapanUrl = 'https://sycm.taobao.com/mq/overview/reportTrend.json?cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&indexCode=uv|searchUvCnt|payPct|payItemQty&seller=-1&token=9a0425930&_={t}'
    # 单品牌
    # brandUrl = 'https://sycm.taobao.com/mq/brandDetail/listTrendByIndexs.json?brandId=30652&cateId=50002804&dateRange=2018-07-15%7C2018-07-15&dateType=recent1&device=0&index=payPct,payRate,uv,payItemQty&seller=-1&token=9a0425930&_=1531712118300'
    brandUrl = 'https://sycm.taobao.com/mq/brandDetail/listTrendByIndexs.json?brandId=30652,30844,5725958,3222885&cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&index={index}&seller=-1&token=9a0425930&_={t}'
    # 炒锅多两个品
    brandcgUrl = 'https://sycm.taobao.com/mq/brandDetail/listTrendByIndexs.json?brandId=30652,30844,5725958,3222885,531544226,1344359932&cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&index={index}&seller=-1&token=9a0425930&_={t}'



    def start_requests(self):

        # 行业大盘

        print(self.dateRange)
        for cate in _CATEID:
            category, cateId = cate.split('/')
            dapan_url = self.dapanUrl.format(cateId=cateId, dateRange=self.dateRange, dateType=self.dateType, t=time_stamp())
            # dapan_url = self.dapanUrl.format(cateId=cateId, dateRange=self.dateRange, dateType='day', t=time_stamp())

            yield scrapy.Request(
                dapan_url,
                headers={
                    'Referer': 'https://sycm.taobao.com/mq/industry/overview/overview.htm?spm=a21ag.7749227.LeftMenu.d293.20b8140dMMIoAZ',
                },
                callback=self.parse_dapan,
                meta={'category': category, 'mark': 'dapan'}
            )
            # 单品牌
            for index in _INDEXS:
                if '炒锅' == category:
                    brand_url = self.brandcgUrl.format(cateId=cateId, dateRange=self.dateRange, dateType=self.dateType, index=index, t=time_stamp())
                    # brand_url = self.brandcgUrl.format(cateId=cateId, dateRange=self.dateRange, dateType='day', index=index, t=time_stamp())
                else:
                    brand_url = self.brandUrl.format(cateId=cateId, dateRange=self.dateRange, dateType=self.dateType, index=index, t=time_stamp())
                    # brand_url = self.brandUrl.format(cateId=cateId, dateRange=self.dateRange, dateType='day', index=index, t=time_stamp())
                yield scrapy.Request(
                    brand_url,
                    headers={
                        'Referer': 'https://sycm.taobao.com/mq/industry/brand/detail.htm?spm=a21ag.7749233.0.0.52104710Z0OchQ',
                    },
                    callback=self.parse_brand,
                    meta={'category': category, 'mark': 'brand', 'cateId': cateId}
                )



    def parse_dapan(self, response):
        '''行业大盘'''
        data_meta = response.meta

        jsonp = json.loads(response.text)

        if 'hasError' not in jsonp:

            logging.error('brand may be cookie error')

        else:
            item_dict = dict()
            item_dict['category'] = data_meta['category']
            item_dict['mark'] = data_meta['mark']
            data_list = jsonp['content']['data']
            for data in data_list:
                item_dict[data['indexCode']] = data['values'][-1]
            # print('dapan==============', item_dict)
            item_dict['time_date'] = self.start_time
            # item_dict['time_date'] = self._time
            yield item_dict

    def parse_brand(self, response):
        '''单品牌'''
        data_meta = response.meta
        item_dict = dict()

        jsonp = json.loads(response.text)

        if 'hasError' not in jsonp:

            logging.error('brand may be cookie error')

        else:

            data_list = jsonp['content']['data']

            try:
                ok = data_meta['next']
            except:
                item_dict['category'] = data_meta['category']
                item_dict['mark'] = data_meta['mark']
                for data in data_list:
                    _dict = dict()
                    _dict['uv'] = data['brandTrend']['uv'][-1]
                    _dict['payItemQty'] = data['brandTrend']['payItemQty'][-1]
                    _dict['payPct'] = data['brandTrend']['payPct'][-1]
                    _dict['payRate'] = data['brandTrend']['payRate'][-1]

                    item_dict[data['brandId']] = _dict
                    item_dict['next'] = 'ok'
                # print('before=================', item_dict)
                if '炒锅' == data_meta['category']:
                    nextUrl = self.brandcgUrl.format(cateId=data_meta['cateId'], dateRange=self.dateRange, dateType=self.dateType, index='searchUvCnt', t=time_stamp())
                    # nextUrl = self.brandcgUrl.format(cateId=data_meta['cateId'], dateRange=self.dateRange, dateType='day', index='searchUvCnt', t=time_stamp())
                else:
                    nextUrl = self.brandUrl.format(cateId=data_meta['cateId'], dateRange=self.dateRange, dateType=self.dateType, index='searchUvCnt', t=time_stamp())
                    # nextUrl = self.brandUrl.format(cateId=data_meta['cateId'], dateRange=self.dateRange, dateType='day', index='searchUvCnt', t=time_stamp())
                yield scrapy.Request(
                    # self.brandUrl.format(cateId=data_meta['cateId'], dateRange=self.dateRange, dateType=self.dateType, index='searchUvCnt', t=time_stamp()),
                    nextUrl,
                    headers={
                        'Referer': 'https://sycm.taobao.com/mq/industry/brand/detail.htm?spm=a21ag.7749233.0.0.52104710Z0OchQ',
                    },
                    callback=self.parse_brand,
                    meta=item_dict,
                )

            else:
                data_list = jsonp['content']['data']
                item_dict['category'] = data_meta['category']
                item_dict['mark'] = data_meta['mark']
                for data in data_list:
                    data_meta[data['brandId']]['searchUvCnt'] = data['brandTrend']['searchUvCnt'][-1]
                    item_dict[data['brandId']] = data_meta[data['brandId']]

                # print('after===================', item_dict)
                item_dict['time_date'] = self.start_time
                # item_dict['time_date'] = self._time
                yield item_dict






