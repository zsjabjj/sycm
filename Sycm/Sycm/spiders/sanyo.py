# -*- coding: utf-8 -*-
import calendar
import datetime
import io
import json
import logging
import sys

import scrapy

from Sycm.pipelines import SanyoPipeline
from Sycm.settings import custom_settings_for_sanyo, WASHER_BRANDS, BS_BRANDS, CATEIDS, FRIDGE_BRANDS
from utils.DateRangeAndTimeStamp import time_stamp, date_range, sanyo_time


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SanyoSpider(scrapy.Spider):

    pipeline = {SanyoPipeline, }
    custom_settings = custom_settings_for_sanyo

    name = 'sanyo'
    allowed_domains = ['sycm.taobao.com']



    # start_urls = ['https://sycm.taobao.com/']
    base_url = 'https://sycm.taobao.com/'

    # top50Url = 'ipoll/live/rank/getHotOfferRank.json?device=0&index=gmv&keywords=null&limit=30&page={page}&token=1e1085e7d&_={t}'
    # 首页 月month 周week 日day
    homePageUrl = 'portal/coreIndex/getShopMainIndexes.json?dateRange={dateRange}&dateType={dateType}&device=0&_={t}&token=8a416f30f'
    # 品牌 自然日day 自然周week 自然月month 自定义range 最近一天recent1 最近7天recent7 最近30天recent30
    brandUrl = 'mq/brandDetail/getSummary.json?brandId={brandId}&cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&seller=1&token=8a416f30f&_={t}'
    # 行业 自然日day 自然周week 自然月month 自定义range 最近一天recent1 最近7天recent7 最近30天recent30
    industryUrl = 'mq/overview/reportIndex.json?cateId={cateId}&dateRange={dateRange}&dateType={dateType}&device=0&indexCode=uv|searchUvCnt|searchClkRate|favBuyerCnt|addCartBuyerCnt|payPct|payItemQty&seller=1&token=8a416f30f&_={t}'

    # def __init__(self, category=None, *args, **kwargs):
    #     super(SanyoSpider, self).__init__(*args, **kwargs)
    #     self.cookie = category



    def start_requests(self):
        '''拼接起始url'''

        for i in ['1', '4']:
            # 时间范围
            start_time, end_time, dateType, index = sanyo_time(i)
            dateRange = start_time + '%7C' + end_time
            # if '1' == i:
            #     start_time, end_time, dateType, index = ('2018-07-14', '2018-07-14', 'day', '')
            #     dateRange = start_time + '%7C' + end_time
            # # print(dateRange)
            # elif '4' == i:
            #     start_time, end_time, dateType, index = ('2018-07-01', '2018-07-14', 'range', '')
            #     dateRange = start_time + '%7C' + end_time

            print(dateRange)

            # dateRanges_day = ['2018-07-1{}%7C2018-07-1{}'.format(no, no) for no in ['3', '4'] if '1' == i]
            # dateRanges_range = ['2018-07-01%7C2018-07-1{}'.format(no) for no in ['3', '4'] if '4' == i]





            # 品牌分析
            for cate in CATEIDS:
                # 洗衣机
                if 'washer' in cate:
                    # 品牌分析
                    for washer in WASHER_BRANDS:
                        brandId = BS_BRANDS[washer]

                        brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=cate['washer'], dateRange=dateRange, dateType=dateType, t=time_stamp())

                        yield scrapy.Request(
                            brand_url,
                            # headers={
                            #     'Cookie': self.cookie,
                            # },
                            callback=self.parse_brand,
                            meta={
                                'cate': 'washer',
                                'brand': washer,
                                'index': i,
                            },
                        )

                # 冰箱
                elif 'fridge' in cate:
                    # 品牌分析
                    for fridge in FRIDGE_BRANDS:
                        brandId = BS_BRANDS[fridge]

                        brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=cate['fridge'], dateRange=dateRange, dateType=dateType, t=time_stamp())

                        yield scrapy.Request(
                            brand_url,
                            # headers={
                            #     'Cookie': self.cookie,
                            # },
                            callback=self.parse_brand,
                            meta={
                                'cate': 'fridge',
                                'brand': fridge,
                                'index': i,
                            },
                        )


        # # 品牌分析
        # for fridge in FRIDGE_BRANDS:
        # # for fridge in WASHER_BRANDS:
        #     brandId = BS_BRANDS[fridge]
        #
        #     # for year in [2017, 2018]:
        #     #
        #     #     if year == 2017:
        #     #         for month in range(2, 13):
        #     #
        #     #             monthRange = calendar.monthrange(year, month)
        #     #             start_time = datetime.date(year=year, month=month, day=1).strftime('%Y-%m-%d')
        #     #             end_time = datetime.date(year=year, month=month, day=monthRange[1]).strftime('%Y-%m-%d')
        #     #
        #     #             dateRange = start_time + '%7C' + end_time
        #     #
        #     #             # brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=50003881,
        #     #             brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=350301,
        #     #                                                              dateRange=dateRange, dateType='month',
        #     #                                                              t=time_stamp())
        #     #             print('dateRange:', dateRange)
        #     #             print('brand_url:', brand_url)
        #     #
        #     #             yield scrapy.Request(
        #     #                 brand_url,
        #     #                 callback=self.parse_new,
        #     #                 meta={
        #     #                     'cate': 'fridge',
        #     #                     'brand': fridge,
        #     #                     'year': year,
        #     #                     'month': month,
        #     #                 },
        #     #             )
        #     # elif year == 2018:
        #     # for month in range(1, 5):
        #     year = 2018
        #     month = 5
        #     monthRange = calendar.monthrange(year, month)
        #     start_time = datetime.date(year=year, month=month, day=1).strftime('%Y-%m-%d')
        #     end_time = datetime.date(year=year, month=month, day=monthRange[1]).strftime('%Y-%m-%d')
        #
        #     dateRange = start_time + '%7C' + end_time
        #
        #     brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=50003881, dateRange=dateRange, dateType='month', t=time_stamp())
        #     # brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=350301, dateRange=dateRange, dateType='month', t=time_stamp())
        #
        #     yield scrapy.Request(
        #         brand_url,
        #         callback=self.parse_new,
        #         meta={
        #             'cate': 'fridge',
        #             'brand': fridge,
        #             'year': year,
        #             'month': month,
        #         },
        #     )

        # for washer in WASHER_BRANDS:
            # brandId = BS_BRANDS[washer]


        # # 行业大盘2016-2018
        # for year in [2016, 2017, 2018]:
        #     if year == 2016:
        #         for month in range(1, 13):
        #             monthRange = calendar.monthrange(year, month)
        #             for day in range(1, monthRange[1] + 1):
        #                 time_date = datetime.date(year=year, month=month, day=day).strftime('%Y-%m-%d')
        #                 dateRange = time_date + '%7C' + time_date
        #
        #                 industry_url = self.base_url + self.industryUrl.format(cateId=350301, dateRange=dateRange, dateType='day', t=time_stamp())
        #                 print('dateRange:', dateRange)
        #                 print('brand_url:', industry_url)
        #
        #                 yield scrapy.Request(
        #                     industry_url,
        #                     callback=self.parse_dapan,
        #                     meta={
        #                         'cate': 'washer',
        #                         # 'brand': washer,
        #                         'year': year,
        #                         'month': month,
        #                         'day': day,
        #                     },
        #                 )
        #
        #
        #             pass
        #         pass
        #     elif year == 2017:
        #         for month in range(1, 13):
        #
        #             monthRange = calendar.monthrange(year, month)
        #             for day in range(1, monthRange[1] + 1):
        #                 time_date = datetime.date(year=year, month=month, day=day).strftime('%Y-%m-%d')
        #                 dateRange = time_date + '%7C' + time_date
        #
        #                 industry_url = self.base_url + self.industryUrl.format(cateId=350301, dateRange=dateRange,
        #                                                                        dateType='day', t=time_stamp())
        #                 print('dateRange:', dateRange)
        #                 print('brand_url:', industry_url)
        #
        #                 yield scrapy.Request(
        #                     industry_url,
        #                     callback=self.parse_dapan,
        #                     meta={
        #                         'cate': 'washer',
        #                         # 'brand': washer,
        #                         'year': year,
        #                         'month': month,
        #                         'day': day,
        #                     },
        #                 )
        #     elif year == 2018:
        #         for month in range(1, 6):
        #
        #             monthRange = calendar.monthrange(year, month)
        #             for day in range(1, monthRange[1] + 1):
        #                 time_date = datetime.date(year=year, month=month, day=day).strftime('%Y-%m-%d')
        #                 dateRange = time_date + '%7C' + time_date
        #
        #                 industry_url = self.base_url + self.industryUrl.format(cateId=350301, dateRange=dateRange,
        #                                                                        dateType='day', t=time_stamp())
        #                 print('dateRange:', dateRange)
        #                 print('brand_url:', industry_url)
        #
        #                 yield scrapy.Request(
        #                     industry_url,
        #                     callback=self.parse_dapan,
        #                     meta={
        #                         'cate': 'washer',
        #                         # 'brand': washer,
        #                         'year': year,
        #                         'month': month,
        #                         'day': day,
        #                     },
        #                 )




        # dateRange = self.start_time + '%7C' + self.end_time
        # print(dateRange)


        # url = self.base_url + self.homePageUrl.format(t=time_stamp())
        # yield scrapy.Request(
        #     url,
        # )

    def parse(self, response):
        '''首页支付金额'''
        # print(response.text)
        print(response.url)
        jsonp = json.loads(response.text)
        # print(jsonp)
        # print(jsonp['hasError'])
        if 'hasError' not in jsonp:
            # cookie = input('cookie:')
            logging.error('home may be cookie error')
        else:
            # yesterday dict
            yesterday_dict = dict()
            yesterday = jsonp['content']['data']['data']['yesterday']
            # 支付金额（元）
            yesterday_dict['home_payAmt'] = yesterday['payAmt']
            # 访客数
            yesterday_dict['home_uv'] = yesterday['uv']
            # 标记
            yesterday_dict['mark'] = 'home'

            yield yesterday_dict

            # 品牌分析
            for cate in CATEIDS:
                # 洗衣机
                if 'washer' in cate:
                    # 行业分析
                    industry_url = self.base_url + self.industryUrl.format(cateId=cate['washer'], dateRange=self.dateRange, dateType=self.dateType, t=time_stamp())

                    yield scrapy.Request(
                        industry_url,
                        callback=self.parse_industry,
                        meta={
                            'cate': 'washer',
                        },
                    )

                    # 品牌分析
                    for washer in WASHER_BRANDS:
                        brandId = BS_BRANDS[washer]

                        brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=cate['washer'], dateRange=self.dateRange, dateType=self.dateType, t=time_stamp())

                        yield scrapy.Request(
                            brand_url,
                            callback=self.parse_brand,
                            meta={
                                'cate': 'washer',
                                'brand': washer,
                            },
                        )
                # 冰箱
                elif 'fridge' in cate:
                    # 行业分析
                    industry_url = self.base_url + self.industryUrl.format(cateId=cate['fridge'], dateRange=self.dateRange, dateType=self.dateType, t=time_stamp())

                    yield scrapy.Request(
                        industry_url,
                        callback=self.parse_industry,
                        meta={
                            'cate': 'fridge',
                        },
                    )
                    # 品牌分析
                    for fridge in FRIDGE_BRANDS:
                        brandId = BS_BRANDS[fridge]

                        brand_url = self.base_url + self.brandUrl.format(brandId=brandId, cateId=cate['fridge'], dateRange=self.dateRange, dateType=self.dateType, t=time_stamp())

                        yield scrapy.Request(
                            brand_url,
                            callback=self.parse_brand,
                            meta={
                                'cate': 'fridge',
                                'brand': fridge,
                            },
                        )

            pass

    def parse_brand(self, response):
        '''品牌分析'''
        jsonp = json.loads(response.text)

        if 'hasError' not in jsonp:
            # cookie = input('cookie:')
            logging.error('brand may be cookie error')
        # 洗衣机品牌
        elif 'washer' == response.meta['cate']:
            item_washer = dict()
            washer_dict = jsonp['content']['data']
            if washer_dict:
                # 交易指数tradeIndex 302518
                item_washer['tradeIndex'] = washer_dict['tradeIndex']
                # 支付商品数payItemCnt 230
                item_washer['payItemCnt'] = washer_dict['payItemCnt']
                # 客单价payPct 1270.86
                item_washer['payPct'] = washer_dict['payPct']
                # 支付转化率payRate 0.0224
                item_washer['payRate'] = washer_dict['payRate']
                # 访客数uv 72997
                item_washer['uv'] = washer_dict['uv']
                # 搜索点击人数searchUvCnt 29790
                item_washer['searchUvCnt'] = washer_dict['searchUvCnt']
                # 收藏人数favBuyerCnt 2987
                item_washer['favBuyerCnt'] = washer_dict['favBuyerCnt']
                # 加购人数addCartUserCnt 6350
                item_washer['addCartUserCnt'] = washer_dict['addCartUserCnt']
                # 卖家数sellerCnt 390
                item_washer['sellerCnt'] = washer_dict['sellerCnt']
                # 被支付卖家数paySellerCnt 65
                item_washer['paySellerCnt'] = washer_dict['paySellerCnt']
                # 重点卖家数majorSellerCnt 44
                item_washer['majorSellerCnt'] = washer_dict['majorSellerCnt']
                # 重点商品数majorItemCnt 50
                item_washer['majorItemCnt'] = washer_dict['majorItemCnt']
                # 品牌
                item_washer['brand'] = response.meta['brand']
                # 分类
                item_washer['cate'] = response.meta['cate']
                # 标记
                item_washer['mark'] = 'brand'
                # 每日累计区分
                item_washer['index'] = response.meta['index']

                yield item_washer
            else:
                logging.error('brand may be cookie error')

        # 冰箱品牌
        elif 'fridge' == response.meta['cate']:
            item_fridge = dict()
            fridge_dict = jsonp['content']['data']
            if fridge_dict:
                # 交易指数tradeIndex 302518
                item_fridge['tradeIndex'] = fridge_dict['tradeIndex']
                # 支付商品数payItemCnt 230
                item_fridge['payItemCnt'] = fridge_dict['payItemCnt']
                # 客单价payPct 1270.86
                item_fridge['payPct'] = fridge_dict['payPct']
                # 支付转化率payRate 0.0224
                item_fridge['payRate'] = fridge_dict['payRate']
                # 访客数uv 72997
                item_fridge['uv'] = fridge_dict['uv']
                # 搜索点击人数searchUvCnt 29790
                item_fridge['searchUvCnt'] = fridge_dict['searchUvCnt']
                # 收藏人数favBuyerCnt 2987
                item_fridge['favBuyerCnt'] = fridge_dict['favBuyerCnt']
                # 加购人数addCartUserCnt 6350
                item_fridge['addCartUserCnt'] = fridge_dict['addCartUserCnt']
                # 卖家数sellerCnt 390
                item_fridge['sellerCnt'] = fridge_dict['sellerCnt']
                # 被支付卖家数paySellerCnt 65
                item_fridge['paySellerCnt'] = fridge_dict['paySellerCnt']
                # 重点卖家数majorSellerCnt 44
                item_fridge['majorSellerCnt'] = fridge_dict['majorSellerCnt']
                # 重点商品数majorItemCnt 50
                item_fridge['majorItemCnt'] = fridge_dict['majorItemCnt']
                # 品牌
                item_fridge['brand'] = response.meta['brand']
                # 分类
                item_fridge['cate'] = response.meta['cate']
                # 标记
                item_fridge['mark'] = 'brand'
                # 每日累计区分
                item_fridge['index'] = response.meta['index']


                yield item_fridge

            else:
                logging.error('brand may be cookie error')

    def parse_industry(self, response):
        '''行业分析'''
        jsonp = json.loads(response.text)

        if 'hasError' not in jsonp:
            # cookie = input('cookie:')
            logging.error('industry may be cookie error')
        # 洗衣机品牌
        elif 'washer' == response.meta['cate']:

            washer_list = jsonp['content']['data']
            if washer_list:
                for washer_dict in washer_list:
                    item_washer = dict()
                    # 分为：访客数uv，搜索点击人数searchUvCnt，搜索点击率searchClkRate，收藏人数favBuyerCnt，加购人数addCartBuyerCnt，客单价payPct，支付件数payItemQty

                    item_washer[washer_dict['indexCode']] = washer_dict['currentValue']
                    item_washer['cate'] = response.meta['cate']
                    # 标记
                    item_washer['mark'] = 'industry'

                    yield item_washer

            else:
                logging.error('industry may be cookie error')

        # 冰箱品牌
        elif 'fridge' == response.meta['cate']:
            fridge_list = jsonp['content']['data']
            if fridge_list:
                for fridge_dict in fridge_list:
                    item_fridge = dict()
                    # 分为：访客数uv，搜索点击人数searchUvCnt，搜索点击率searchClkRate，收藏人数favBuyerCnt，加购人数addCartBuyerCnt，客单价payPct，支付件数payItemQty

                    item_fridge[fridge_dict['indexCode']] = fridge_dict['currentValue']
                    item_fridge['cate'] = response.meta['cate']
                    # 标记
                    item_fridge['mark'] = 'industry'

                    yield item_fridge

            else:
                logging.error('industry may be cookie error')

    def parse_new(self, response):
        print('parse_url:', response.url)
        print('brand:', response.meta['brand'])
        # print(response.text)
        jsonp = json.loads(response.text)
        # print(response.meta['brand'], jsonp['hasError'])

        if 'hasError' not in jsonp:
            # cookie = input('cookie:')
            logging.error('brand may be cookie error')
        # 洗衣机品牌
        # elif 'washer' == response.meta['cate']:
        else:
            item_fridge = dict()
            fridge_dict = jsonp['content']['data']
            if fridge_dict:
                # 交易指数tradeIndex 302518
                # item_fridge['tradeIndex'] = fridge_dict['tradeIndex']
                # 支付商品数payItemCnt 230
                item_fridge['payItemCnt'] = fridge_dict['payItemCnt']
                # 客单价payPct 1270.86
                item_fridge['payPct'] = fridge_dict['payPct']
                # 支付转化率payRate 0.0224
                item_fridge['payRate'] = fridge_dict['payRate']
                # 访客数uv 72997
                item_fridge['uv'] = fridge_dict['uv']
                # 搜索点击人数searchUvCnt 29790
                # item_fridge['searchUvCnt'] = fridge_dict['searchUvCnt']
                # 收藏人数favBuyerCnt 2987
                item_fridge['favBuyerCnt'] = fridge_dict['favBuyerCnt']
                # 加购人数addCartUserCnt 6350
                item_fridge['addCartUserCnt'] = fridge_dict['addCartUserCnt']
                # 卖家数sellerCnt 390
                # item_fridge['sellerCnt'] = fridge_dict['sellerCnt']
                # 被支付卖家数paySellerCnt 65
                # item_fridge['paySellerCnt'] = fridge_dict['paySellerCnt']
                # 重点卖家数majorSellerCnt 44
                # item_fridge['majorSellerCnt'] = fridge_dict['majorSellerCnt']
                # 重点商品数majorItemCnt 50
                # item_fridge['majorItemCnt'] = fridge_dict['majorItemCnt']
                # 品牌
                item_fridge['brand'] = response.meta['brand']
                # 分类
                item_fridge['cate'] = response.meta['cate']
                # 标记
                item_fridge['mark'] = 'brand'
                # 年
                item_fridge['year'] = response.meta['year']
                # 月
                item_fridge['month'] = response.meta['month']

                yield item_fridge
            else:
                logging.error('brand may be cookie error')

        pass


    def parse_dapan(self, response):
        print('parse_url:', response.url)
        # print('brand:', response.meta['brand'])
        # print(response.text)
        jsonp = json.loads(response.text)
        # print(response.meta['brand'], jsonp['hasError'])

        if 'hasError' not in jsonp:
            # cookie = input('cookie:')
            logging.error('brand may be cookie error')
        # 洗衣机品牌
        # elif 'washer' == response.meta['cate']:
        else:
            # item_fridge = dict()
            washer_list = jsonp['content']['data']
            if washer_list:
                item_washer = dict()
                for washer_dict in washer_list:
                    # item_washer = dict()
                    # 分为：访客数uv，搜索点击人数searchUvCnt，搜索点击率searchClkRate，收藏人数favBuyerCnt，加购人数addCartBuyerCnt，客单价payPct，支付件数payItemQty

                    item_washer[washer_dict['indexCode']] = washer_dict['currentValue']
                item_washer['cate'] = response.meta['cate']
                item_washer['year'] = response.meta['year']
                item_washer['month'] = response.meta['month']
                item_washer['day'] = response.meta['day']

                # 标记
                item_washer['mark'] = 'industry'

                print('parse_dict:', item_washer)

                yield item_washer

            else:
                logging.error('industry may be cookie error')

        pass

