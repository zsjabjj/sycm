# -*- coding: utf-8 -*-
import json
import logging

import scrapy

from Sycm.pipelines import SanyoPipeline
from Sycm.settings import custom_settings_for_sanyort
from utils.DateRangeAndTimeStamp import time_stamp


class SanyortSpider(scrapy.Spider):

    pipeline = {SanyoPipeline, }
    custom_settings = custom_settings_for_sanyort

    name = 'sanyoRT'
    allowed_domains = ['sycm.taobao.com']
    # start_urls = ['http://sycm.taobao.com/']

    base_url = 'https://sycm.taobao.com/'

    top50Url = 'ipoll/live/rank/getHotOfferRank.json?device=0&index=gmv&keywords=null&limit=30&page={page}&token=85463cb8f&_={t}'

    def start_requests(self):
        '''拼接起始url'''

        url = self.base_url + self.top50Url.format(page=1, t=time_stamp())
        yield scrapy.Request(
            url,
        )

    def parse(self, response):
        '''实时支付金额top50'''
        jsonp = json.loads(response.text)

        if '操作成功' == jsonp['message']:

            totalPage = jsonp['data']['data']['totalPage']
            page = jsonp['data']['data']['page']
            top50_list = jsonp['data']['data']['list']

            if top50_list:
                for top50 in top50_list:
                    top50_dict = dict()
                    # 浏览量
                    top50_dict['top50_pv'] = top50['pv']
                    # 访客数
                    top50_dict['top50_uv'] = top50['uv']
                    # 支付金额
                    top50_dict['top50_gmv'] = top50['gmv'] / 100
                    # 支付买家数
                    top50_dict['top50_buyerCnt'] = top50['buyerCnt']
                    # 支付转化率
                    top50_dict['top50_payRate'] = top50['payRate']
                    # 标题
                    top50_dict['top50_title'] = top50['itemModel']['title']
                    # 发布时间
                    top50_dict['top50_startsStr'] = top50['itemModel']['startsStr']

                    yield top50_dict

                if page < totalPage:
                    next_url = self.base_url + self.top50Url.format(page=page + 1, t=time_stamp())

                    yield scrapy.Request(
                        next_url,
                        callback=self.parse,
                    )

        else:
            logging.info(response.text)
            logging.error('may be cookie error or get url too fast')
