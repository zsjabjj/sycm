# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SycmItem(scrapy.Item):
    # define the fields for your item here like:
    modelName = scrapy.Field()
    brandName = scrapy.Field()
    brandId = scrapy.Field()
    spuId = scrapy.Field()
    modelId = scrapy.Field()
    device_category = scrapy.Field()
    info = scrapy.Field()


class TrendItem(scrapy.Item):
    '''曲线数据item'''
    modelName = scrapy.Field()
    brandName = scrapy.Field()
    brandId = scrapy.Field()
    spuId = scrapy.Field()
    modelId = scrapy.Field()
    device_category = scrapy.Field()
    info = scrapy.Field()
    itemId = scrapy.Field()
    payByrRateIndex = scrapy.Field()
    payOrdCnt = scrapy.Field()
    payItemQty = scrapy.Field()
    date_time = scrapy.Field()
    num = scrapy.Field()
    total = scrapy.Field()


class SrcFlowItem(scrapy.Item):
    '''流量item'''
    modelName = scrapy.Field()
    brandName = scrapy.Field()
    brandId = scrapy.Field()
    spuId = scrapy.Field()
    modelId = scrapy.Field()
    device_category = scrapy.Field()
    info = scrapy.Field()
    itemId = scrapy.Field()
    i = scrapy.Field()
    pc = scrapy.Field()
    wifi = scrapy.Field()


class SanyoHomeItem(scrapy.Item):
    '''首页item'''
    # 支付金额（元）
    home_payAmt = scrapy.Field()
    # 访客数
    home_uv = scrapy.Field()
    # 标记
    mark = scrapy.Field()
    pass


class SanyoBrandItem(scrapy.Item):
    '''品牌'''

    # 交易指数
    tradeIndex = scrapy.Field()
    # 支付商品数
    payItemCnt = scrapy.Field()
    # 客单价
    payPct = scrapy.Field()
    # 支付转化率
    payRate = scrapy.Field()
    # 访客数
    uv = scrapy.Field()
    # 搜索点击人数
    searchUvCnt = scrapy.Field()
    # 收藏人数
    favBuyerCnt = scrapy.Field()
    # 加购人数
    addCartUserCnt = scrapy.Field()
    # 卖家数
    sellerCnt = scrapy.Field()
    # 被支付卖家数
    paySellerCnt = scrapy.Field()
    # 重点卖家数
    majorSellerCnt = scrapy.Field()
    # 重点商品数
    majorItemCnt = scrapy.Field()
    # 品牌
    brand = scrapy.Field()

    # 分类
    cate = scrapy.Field()
    # 标记
    mark = scrapy.Field()
    # 年
    year = scrapy.Field()
    # 月
    month = scrapy.Field()
    # 每日累计
    index = scrapy.Field()

    pass


class SanyoIndustryItem(scrapy.Item):
    '''行业'''
    # 访客数uv，
    uv = scrapy.Field()
    # 搜索点击人数searchUvCnt，
    searchUvCnt = scrapy.Field()
    # 搜索点击率searchClkRate，
    searchClkRate = scrapy.Field()
    # 收藏人数favBuyerCnt，
    favBuyerCnt = scrapy.Field()
    # 加购人数addCartBuyerCnt，
    addCartBuyerCnt = scrapy.Field()
    # 客单价payPct，
    payPct = scrapy.Field()
    # 支付件数payItemQty
    payItemQty = scrapy.Field()

    # 分类
    cate = scrapy.Field()
    # 标记
    mark = scrapy.Field()

    pass


class MideaItem(scrapy.Item):
    '''行业 '''
    # 访客数uv，
    uv = scrapy.Field()
    # 搜索点击人数searchUvCnt，
    searchUvCnt = scrapy.Field()
    # 支付转化率payRate，
    payRate = scrapy.Field()
    # 客单价payPct，
    payPct = scrapy.Field()
    # 支付件数payItemQty
    payItemQty = scrapy.Field()

    # 分类
    category = scrapy.Field()
    # 标记
    mark = scrapy.Field()
    # 日期
    time_date = scrapy.Field()

    pass


class SanyoRTItem(scrapy.Item):
    '''实时数据item'''
    # 浏览量
    top50_pv = scrapy.Field()
    # 访客数
    top50_uv = scrapy.Field()
    # 支付金额
    top50_gmv = scrapy.Field()
    # 支付买家数
    top50_buyerCnt = scrapy.Field()
    # 支付转化率
    top50_payRate = scrapy.Field()
    # 标题
    top50_title = scrapy.Field()
    # 发布时间
    top50_startsStr = scrapy.Field()

    pass
