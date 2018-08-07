# -*- coding: utf-8 -*-
import datetime
import io
import json
import logging
import sys

import scrapy

from Sycm.pipelines import SycmAllPipeline
from Sycm.settings import BRANDIDS, custom_settings_for_ctmall
from utils.DateRangeAndTimeStamp import date_range, time_stamp, date_range_pre
from utils.FileToDict import file_dict


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class CtmallSpider(scrapy.Spider):

    print('ctmall')

    pipeline = {SycmAllPipeline, }
    custom_settings = custom_settings_for_ctmall

    name = 'ctmall'
    allowed_domains = ['sycm.taobao.com']
    # start_urls = ['http://tmall.com/']
    base_url = 'https://sycm.taobao.com/mq/'



    # 时间范围
    start_time, end_time, dateType, index = date_range()
    dateRange = start_time + '%7C' + end_time
    print(dateRange)
    # 默认时间范围
    # start_time_pre, end_time_pre = date_range_pre()
    start_time_pre, end_time_pre, dateTypePre = start_time, end_time, dateType
    dateRangePre = start_time_pre + '%7C' + end_time_pre
    print(dateRangePre)

    brandListUrl = 'industry/product/product_rank/getRankList.json?brandId={brandId}&cateId=50012082&dateRange={dateRange}&dateType={dateType}&device=0&seller=1&token=f400b7b0f&_={t}'
    itemIdUrl = 'rank/listItem.json?brandId={brandId}&cateId=50012082&categoryId=50012082&dateRange={dateRange}&dateRangePre={dateRangePre}&dateType={dateType}&dateTypePre=recent1&device=0&devicePre=0&itemDetailType=5&keyword=&modelId={modelId}&orderDirection=desc&orderField=payOrdCnt&page=1&pageSize=15&rankTabIndex=0&rankType=1&seller=1&spuId={spuId}&token=f400b7b0f&view=rank&_={t}'
    itemTrendUrl = 'rank/listItemTrend.json?brandId={brandId}&cateId=50012082&categoryId=50012082&dateRange={dateRange}&dateRangePre={dateRangePre}&dateType={dateType}&dateTypePre=recent1&device=0&devicePre=0&indexes=payOrdCnt,payByrRateIndex,payItemQty&itemDetailType=5&itemId={itemId}&latitude=undefined&modelId={modelId}&rankTabIndex=0&rankType=1&seller=1&spuId={spuId}&token=f400b7b0f&view=detail&_={t}'
    itemSrcFlowUrl = 'rank/listItemSrcFlow.json?brandId={brandId}&cateId=50012082&categoryId=50012082&dateRange={dateRange}&dateRangePre={dateRangePre}&dateType={dateType}&dateTypePre={dateTypePre}&device={device}&devicePre=0&itemDetailType=5&itemId={itemId}&modelId={modelId}&rankTabIndex=0&rankType=1&seller=1&spuId={spuId}&token=f400b7b0f&view=detail&_={t}'

    # 建立一个存储列表
    pw_list = list()
    # trend_list = list()

    def start_requests(self):
        '''拼接起始url'''


        # dateRange = self.start_time + '%7C' + self.end_time
        # print(dateRange)

        for brandId in BRANDIDS:
            print(brandId)
            url = self.base_url + self.brandListUrl.format(brandId=brandId, dateRange=self.dateRange, dateType=self.dateType, t=time_stamp())
            yield scrapy.Request(
                url,
                headers={
                    'Referer': 'https://sycm.taobao.com/mq/industry/product/rank.htm?spm=a21ag.7782695.LeftMenu.d320.7ee44653mUqxYv',
                },
            )

    def parse(self, response):
        '''获取品牌型号以及ID，并且进行下一步请求'''
        print(response.url)
        jsonp = json.loads(response.text)
        # print(jsonp)
        # print(jsonp['hasError'])
        if 'hasError' not in jsonp:
            # cookie = input('cookie:')
            logging.error('may be cookie error')
        else:
            # 品牌型号列表
            bm_list = jsonp['content']['data']
            # print('---------', bm_list)
            for bm in bm_list:
                bm_dict, _ = file_dict(bm)

                # print(bm_dict)
                if bm_dict:
                    url = self.base_url + self.itemIdUrl.format(brandId=bm_dict['brandId'], dateRange=self.dateRange, dateType=self.dateType, dateRangePre=self.dateRangePre, modelId=bm_dict['modelId'], spuId=bm_dict['spuId'], t=time_stamp())
                    yield scrapy.Request(
                        url,
                        headers={
                            'Referer': 'https://sycm.taobao.com/mq/industry/rank/spu.htm?spm=a21ag.7782686.0.0.3ffb277512wIuF',
                        },
                        callback=self.parse_itemId,
                        meta=bm_dict,
                    )


    def parse_itemId(self, response):
        '''获取itemId，并且进行下一步请求'''
        # print('=========')
        # 接收上一请求的数据
        data = response.meta
        # 获得的数据转成字典
        jsonp = json.loads(response.text)
        # 判断返回数据是否正确
        if 'hasError' not in jsonp:
            logging.error('may be cookie error')
        else:
            itemId_list = jsonp['content']['data']['data']
            # 判断该商品是否能够查到
            if not itemId_list:
                # 没有查到，直接返回
                item = data
                item['info'] = 'no'
                del item['depth']
                del item['download_timeout']
                del item['download_slot']
                del item['download_latency']
                # print('no1-----------', item)
                yield item
            else:
                # 查到
                ctmall_list = [itemId for itemId in itemId_list if '天猫超市' == itemId['shopName']]
                # 判断是否有猫超
                if not ctmall_list:
                    # 没有猫超
                    item = data
                    item['info'] = 'no'
                    # {'modelName': 'MJ-LZ25Easy203', 'brandName': 'Midea/美的', 'brandId': 30652, 'spuId': 924798040, 'modelId': 924798040, 'device_category': '料理机', 'depth': 1, 'download_timeout': 180.0, 'oad_slot': 'sycm.taobao.com', 'download_latency': 0.10310888290405273, 'info': 'no'}

                    del item['depth']
                    del item['download_timeout']
                    del item['download_slot']
                    del item['download_latency']
                    # print('no2-----------', item)
                    yield item
                else:
                    # 有猫超
                    for ctmall in ctmall_list:
                        data['itemId'] = ctmall['itemId']
                        data['info'] = 'yes'
                        # 请求曲线数据
                        url_trend = self.base_url + self.itemTrendUrl.format(brandId=data['brandId'], dateRange=self.dateRange, dateType=self.dateType, dateRangePre=self.dateRangePre, modelId=data['modelId'], spuId=data['spuId'], t=time_stamp(), itemId=data['itemId'])
                        yield scrapy.Request(
                            url_trend,
                            headers={
                                'Referer': 'https://sycm.taobao.com/mq/industry/rank/spu.htm?spm=a21ag.7782686.0.0.3ffb277512wIuF',
                            },
                            callback=self.parse_trend,
                            meta=data,
                        )
                        # 请求流量数据
                        for i in range(1, 3):
                            data['i'] = i  # int
                            url_srcflow = self.base_url + self.itemSrcFlowUrl.format(brandId=data['brandId'], dateRange=self.dateRange, dateType=self.dateType, dateRangePre=self.dateRangePre, modelId=data['modelId'], spuId=data['spuId'], t=time_stamp(), itemId=data['itemId'], device=i, dateTypePre=self.dateTypePre)
                            yield scrapy.Request(
                                url_srcflow,
                                headers={
                                    'Referer': 'https://sycm.taobao.com/mq/industry/rank/spu.htm?spm=a21ag.7782686.0.0.3ffb277512wIuF',
                                },
                                callback=self.parse_srcflow,
                                meta=data,
                            )

    def parse_trend(self, response):
        '''曲线数据'''
        # 接收上一请求的数据
        data = response.meta
        del data['depth']
        del data['download_timeout']
        del data['download_slot']
        del data['download_latency']
        # 获得的数据转成字典
        jsonp = json.loads(response.text)
        # 判断返回数据是否正确
        if 'hasError' not in jsonp:
            logging.error('may be cookie error')
        else:
            # 转化率
            payByrRateIndexList = jsonp['content']['data']['payByrRateIndexList']
            # 支付订单数
            payOrdCntList = jsonp['content']['data']['payOrdCntList']
            # 支付件数
            payItemQtyList = jsonp['content']['data']['payItemQtyList']

            _1 = len(payByrRateIndexList)
            _2 = len(payOrdCntList)
            _3 = len(payItemQtyList)

            if not all([payByrRateIndexList, payOrdCntList, payItemQtyList]):
                logging.error('may be cookie error')
            # 三者数量一致
            elif _1 == _2 and _2 == _3:
                for num in range(_1 - 1, -1, -1):
                    item = data
                    item['payByrRateIndex'] = payByrRateIndexList[num]
                    item['payOrdCnt'] = payOrdCntList[num]
                    item['payItemQty'] = payItemQtyList[num]
                    item['date_time'] = (datetime.date.today() - datetime.timedelta(days=_1 - num)).strftime('%Y-%m-%d')
                    item['total'] = _1
                    item['num'] = num

                    # print('yes trend-----------', item)
                    yield item
            # 三者数量不一致
            else:
                for num in range(min(_1, _2, _3) - 1, -1, -1):
                    item = data
                    item['payByrRateIndex'] = payByrRateIndexList[num]
                    item['payOrdCnt'] = payOrdCntList[num]
                    item['payItemQty'] = payItemQtyList[num]
                    item['date_time'] = (datetime.date.today() - datetime.timedelta(days=_1 - num)).strftime('%Y-%m-%d')
                    item['total'] = min(_1, _2, _3)
                    item['num'] = num
                    # print('no trend-----------', item)
                    # {'modelName': 'CFXB40FC8533-75', 'brandName': 'Supor/苏泊尔', 'brandId': 30844, 'spuId': 418857858, 'modelId': 418857858, 'device_category': '电饭煲', 'depth': 2, 'download_timeout': 180ownload_slot': 'sycm.taobao.com', 'download_latency': 0.16314172744750977, 'itemId': 529114966678, 'info': 'yes', 'payByrRateIndex': 118.12, 'payOrdCnt': 101, 'payItemQty': 101, 'date_time': '2018-04-23'}
                    yield item


    def parse_srcflow(self, response):
        '''流量数据'''
        # 接收上一请求的数据
        data = response.meta
        # 获得的数据转成字典
        jsonp = json.loads(response.text)
        # print(jsonp)
        # create dict for pc/wifi
        pc_data = dict()
        wifi_data = dict()

        # 判断返回数据是否正确
        if 'hasError' not in jsonp:
            logging.error('may be cookie error')
        elif 1 == data['i']:
            # pc端
            pc_list = jsonp['content']['data']
            pc_dict = dict()
            for pc in pc_list:
                # print('pc字典类型', type(pc))
                # print(pc)
                # pc_json = json.loads(pc)
                # print('转换之后pc', type(pc))
                pc_dict[pc['pageName']] = pc['uv']
            data['pc'] = pc_dict
            del data['depth']
            del data['download_timeout']
            del data['download_slot']
            del data['download_latency']
            pc_data = data
            # print(pc_data)
            self.pw_list.append(pc_data)





        elif 2 == data['i']:
            # 无线端
            wifi_list = jsonp['content']['data']
            wifi_dict = dict()
            for wifi in wifi_list:
                # print('wifi字典类型', type(wifi))
                # print(wifi)
                # wifi_json = json.loads(wifi)
                # print('转换之后wifi', type(wifi))
                wifi_dict[wifi['pageName']] = wifi['uv']
            data['wifi'] = wifi_dict
            del data['depth']
            del data['download_timeout']
            del data['download_slot']
            del data['download_latency']
            wifi_data = data
            # print(wifi_data)
            self.pw_list.append(wifi_data)
        # if pc_data['modelName'] == wifi_data['modelName']:
        #     item = pc_data
        #     item['wifi'] = wifi_data['wifi']
        #     yield item
        # if pc_data:
        #     self.pw_list.append(pc_data)
        # elif wifi_data:
        #     self.pw_list.append(wifi_data)


        for pw in self.pw_list:

            for no in range(self.pw_list.index(pw), len(self.pw_list)):
                pw_no = self.pw_list[no]
                if 'pc' in pw and 'wifi' in pw_no and pw['modelName'] == pw_no['modelName']:

                    item = pw
                    item['wifi'] = pw_no['wifi']
                    self.pw_list.pop(self.pw_list.index(pw))
                    self.pw_list.pop(self.pw_list.index(pw_no))
                    # print('pc srcflow------------', item)
                    yield item
                elif 'wifi' in pw and 'pc' in pw_no and pw['modelName'] == pw_no['modelName']:
                    item = pw
                    item['pc'] = pw_no['pc']
                    self.pw_list.pop(self.pw_list.index(pw))
                    self.pw_list.pop(self.pw_list.index(pw_no))
                    # print('wifi srcflow------------', item)
                    yield item

        # item = data
        #
        # print('srcflow------------', item)
        # # {'modelName': 'C21-SK805', 'brandName': 'Joyoung/九阳', 'brandId': 30850, 'spuId': 248053921, 'modelId': 248053921, 'device_category': '电磁炉', 'depth': 2, 'download_timeout': 180.0,nload_slot': 'sycm.taobao.com', 'download_latency': 0.10880422592163086, 'itemId': 45647212083, 'info': 'yes', 'i': 2, 'wifi': {'淘内免费其他': 120, '手淘搜索': 59, '购物车': 16, '手淘品牌街': 15, '我的淘手淘问大家': 4, '淘宝客': 3, '手淘首页': 2, '聚划算': 1}}
        # yield item











