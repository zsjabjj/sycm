# -*- coding: utf-8 -*-

# Scrapy settings for Sycm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import os
import random

BOT_NAME = 'Sycm'

SPIDER_MODULES = ['Sycm.spiders']
NEWSPIDER_MODULE = 'Sycm.spiders'

# 炒锅，煎锅，奶锅，汤锅，蒸锅
_CATEID = ['炒锅/50002804', '煎锅/50004390', '奶锅/50005480', '汤锅/50002808', '蒸锅/50002807']
_BRAND = {'30652': '美的', '30844': '苏泊尔', '5725958': '炊大皇', '3222885': '爱仕达', '531544226': '臻三环', '1344359932': 'feillers'}
# _INDEXS = ['payPct,payRate,uv,payItemQty', 'searchUvCnt']
_INDEXS = ['payPct,payRate,uv,payItemQty']

# 九阳brandId：30850 美的brandId：30652 苏泊尔brandId：30844
BRANDIDS = ['30850', '30652', '30844']

# 生意参谋洗衣机/冰箱品牌ID
BS_BRANDS = {
    "Haier/海尔": 11016,
    "Littleswan/小天鹅": 30657,
    "Midea/美的": 30652,
    "SIEMENS/西门子": 80946,
    "Samsung/三星": 81156,
    "Bosch/博世": 3223459,
    "Whirlpool/惠而浦": 66878525,
    "Royalstar/荣事达": 30654,
    "DIQUA/帝度": 50878944,
    "Sanyo/三洋": 10728,
    "TCL": 10858,
    "Panasonic/松下": 81147,
    "Leader/统帅": 113190408,
}

CATEIDS = [
    {'washer': 350301},
    {'fridge': 50003881},
]

WASHER_BRANDS = ['Haier/海尔', 'Littleswan/小天鹅', 'Midea/美的', 'SIEMENS/西门子', 'Sanyo/三洋', 'TCL', 'Panasonic/松下', 'Leader/统帅', 'Royalstar/荣事达', 'Whirlpool/惠而浦']
FRIDGE_BRANDS = ['Haier/海尔', 'SIEMENS/西门子', 'Midea/美的', 'Samsung/三星', 'Bosch/博世', 'Whirlpool/惠而浦', 'Royalstar/荣事达', 'DIQUA/帝度']

# 品牌和型号文件路径
# BM_FILE_PATH = 'brand_model.txt'

# ua列表
MY_USER_AGENT_PC = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
]

# 是否启用log日志, 默认开启
# LOG_ENABLED = False
# log编码格式, 默认utf-8
# LOG_ENCODING = ''
# 默认: None，在当前目录里创建logging输出文件的文件名
# 设置日志大小为10m
print('log_file start')
# print('ctmall start')
if os.path.exists('./log/ctmall.log') and os.path.getsize('./log/ctmall.log') >= 1024 * 1024 *10:
   print(os.path.getsize('./log/ctmall.log'))
   os.rename('./log/ctmall.log', './log/ctmall_%s.log' % datetime.datetime.now().strftime("%Y%m%d"))
elif os.path.exists('./log/sanyo.log') and os.path.getsize('./log/sanyo.log') >= 1024 * 1024 *10:
    print(os.path.getsize('./log/sanyo.log'))
    os.rename('./log/sanyo.log', './log/sanyo_%s.log' % datetime.datetime.now().strftime("%Y%m%d"))
elif os.path.exists('./log/midea.log') and os.path.getsize('./log/midea.log') >= 1024 * 1024 *10:
    print(os.path.getsize('./log/midea.log'))
    os.rename('./log/midea.log', './log/midea_%s.log' % datetime.datetime.now().strftime("%Y%m%d"))
elif os.path.exists('./log/sanyort.log') and os.path.getsize('./log/sanyort.log') >= 1024 * 1024 *10:
    print(os.path.getsize('./log/sanyort.log'))
    os.rename('./log/sanyort.log', './log/sanyort_%s.log' % datetime.datetime.now().strftime("%Y%m%d"))
print('log_file end')
# LOG_FILE = './log/ctmall.log'
# 默认: 'DEBUG'，log的最低级别, 如果上线后, 最好将级别调成info
LOG_LEVEL = 'INFO'
# 默认: False 如果为 True，进程所有的标准输出(及错误)将会被重定向到log(如果LOG_FILE开启)中。例如，执行 print "hello" ，其将会在Scrapy log中显示
# LOG_STDOUT = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = random.choice(MY_USER_AGENT_PC),

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# 多个爬虫自定义多个setting
custom_settings_for_ctmall = {
    'DOWNLOAD_DELAY': 0.1,
    'LOG_FILE': './log/ctmall.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'ITEM_PIPELINES': {
        'Sycm.pipelines.SycmAllPipeline': 300,
    },
    'DEFAULT_REQUEST_HEADERS': {
        # 'Referer': 'https://sycm.taobao.com/mq/industry/product/rank.htm?spm=a21ag.7782695.LeftMenu.d320.7ee44653mUqxYv',
      # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   'Accept-Language': 'en',
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/61.0.3163.128 Safari/534.24 XiaoMi/MiuiBrowser/9.7.2 tae_sdk_a_2.1.0 AliApp(BC/2.1.0)',
    #     'Connection': 'keep-alive',
        'Cookie': 't=353065b89f6de4884ac4996fe6b330f1; cna=p06hE64hcF0CAXARX/O1H59e; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; ali_ab=112.17.95.243.1528785183954.3; enc=z114ehbR5%2FL9evDLdagORWxBZKBgR1H5rjGcjfUtKap6zDBWL1gNz5N%2B%2FlU5wPCdN6AacSoQ5vdYP8d7o%2FlkaQ%3D%3D; tg=0; _cc_=W5iHLLyFfA%3D%3D; mt=ci=0_0; cookie2=120f0d52b7bc698f691dc3dd99cd8031; _tb_token_=e6615ae74e631; JSESSIONID=73135610DE6B683774ADBEBB6D3DE280; x=2973966816; uc3=id2=&nk2=&lg2=; uc1=cookie14=UoTfKLACq0xeYQ%3D%3D&lng=zh_CN; skt=b2aab7464a19676e; sn=%E7%BE%8E%E7%9A%84%E7%94%9F%E6%B4%BB%E7%94%B5%E5%99%A8%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%92%9F%E5%A3%B0; unb=3926989410; tracknick=; csg=8686260f; _euacm_ac_l_uid_=3926989410; 3926989410_euacm_ac_c_uid_=2973966816; 3926989410_euacm_ac_rs_uid_=2973966816; _euacm_ac_rs_sid_=286653957; _portal_version_=new; v=0; isg=BLm5R24txsDqz5ocJjeo7Ky4yCNTbvVYMn_Gz9vuM-BfYtn0IxQ3Sb004CYxWkWw',

    },
}

custom_settings_for_sanyo = {
    'DOWNLOAD_DELAY': 3,
    'LOG_FILE': './log/sanyo.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'ITEM_PIPELINES': {
        'Sycm.pipelines.SanyoPipeline': 400,
    },
    'DEFAULT_REQUEST_HEADERS': {
        'Referer': 'https://sycm.taobao.com/mq/industry/brand/detail.htm?spm=a21ag.7749233.0.0.47564710CpQrAv',
    #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 't=353065b89f6de4884ac4996fe6b330f1; cna=p06hE64hcF0CAXARX/O1H59e; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; ali_ab=112.17.95.243.1528785183954.3; enc=z114ehbR5%2FL9evDLdagORWxBZKBgR1H5rjGcjfUtKap6zDBWL1gNz5N%2B%2FlU5wPCdN6AacSoQ5vdYP8d7o%2FlkaQ%3D%3D; tg=0; _cc_=UtASsssmfA%3D%3D; mt=ci=0_0; cookie2=126aae003ef19c88c5a9d73c8f4096a0; _tb_token_=e3bae76b333b1; JSESSIONID=963DA55467A0A04BE3F274FFB6DA0484; x=761383686; uc3=id2=&nk2=&lg2=; uc1=cookie14=UoTfKjMjJ4%2BtQw%3D%3D&lng=zh_CN; skt=a60ee7723ed50be4; sn=%E4%B8%89%E6%B4%8B%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%95%B0%E6%8D%AE%E7%BB%84; unb=3789122802; tracknick=; csg=75079c05; _euacm_ac_l_uid_=3789122802; 3789122802_euacm_ac_c_uid_=761383686; 3789122802_euacm_ac_rs_uid_=761383686; _euacm_ac_rs_sid_=68898854; _portal_version_=new; v=0; apush5c48dd3143d776cb78e4029d2ce08194=%7B%22ts%22%3A1531704257637%2C%22parentId%22%3A1531704251624%7D; isg=BAoK9zD8ZQ5DLenJqRrrMXsdW_ZsU9Z1JboVOpRDet3oR6gBfIqhZDUxU_M-twbt',
    },
}


custom_settings_for_midea = {
    'DOWNLOAD_DELAY': 1,
    'LOG_FILE': './log/midea.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'ITEM_PIPELINES': {
        'Sycm.pipelines.MideaPipeline': 300,
    },
    'DEFAULT_REQUEST_HEADERS': {
        # 'Referer': 'https://sycm.taobao.com/mq/industry/brand/detail.htm?spm=a21ag.7749233.0.0.47564710CpQrAv',
    #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 't=353065b89f6de4884ac4996fe6b330f1; cna=p06hE64hcF0CAXARX/O1H59e; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; ali_ab=112.17.95.243.1528785183954.3; enc=z114ehbR5%2FL9evDLdagORWxBZKBgR1H5rjGcjfUtKap6zDBWL1gNz5N%2B%2FlU5wPCdN6AacSoQ5vdYP8d7o%2FlkaQ%3D%3D; tg=0; _cc_=W5iHLLyFfA%3D%3D; mt=ci=0_0; cookie2=120f0d52b7bc698f691dc3dd99cd8031; _tb_token_=e6615ae74e631; uc3=id2=&nk2=&lg2=; tracknick=; JSESSIONID=73135610DE6B683774ADBEBB6D3DE280; x=2385614665; uc1=cookie14=UoTfKLACq0541g%3D%3D&lng=zh_CN; skt=617b44bd793ece75; sn=%E7%BE%8E%E7%9A%84%E7%82%8A%E5%85%B7%E6%97%97%E8%88%B0%E5%BA%97%3A%E5%8A%A9%E7%90%86; unb=3618417766; csg=49fe89cc; _euacm_ac_l_uid_=3618417766; 3618417766_euacm_ac_c_uid_=2385614665; 3618417766_euacm_ac_rs_uid_=2385614665; _euacm_ac_rs_sid_=116591256; v=0; _portal_version_=new; isg=BLOzZTno7DIctqCuOCny_po-QrEdQB-KpLmcHWVQD1IJZNMG7bjX-hFyGtQvRJ-i',
    },
}

custom_settings_for_sanyort = {
    'DOWNLOAD_DELAY': 0.5,
    'LOG_FILE': './log/sanyort.log',
    # 'CONCURRENT_REQUESTS': 100,
    # 'DOWNLOADER_MIDDLEWARES': {
    #     'spider.middleware_for_spider1.Middleware': 667,
    # },
    'ITEM_PIPELINES': {
        'Sycm.pipelines.SanyoPipeline': 400,
    },
    'DEFAULT_REQUEST_HEADERS': {
        'Referer': 'https://sycm.taobao.com/portal/home.htm',
    #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   'Accept-Language': 'en',
        'Cookie': 't=09d0a59e21c3059e1be220c847b71b0a; cna=Wa9VE42Yoi8CAXARX/Mk4npp; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=162d2ee4cd2a11-01ca86c68c73d1-33697b04-1fa400-162d2ee4cd3dbb; tg=0; l=AvPzoxfP85MORwVh2x7lo1UGA/wdQIfq; ali_ab=112.17.95.243.1524795971924.1; _m_h5_tk=ee2612c47c08f08d6ffc86dc0594753d_1526283678874; _m_h5_tk_enc=966ec13cf4d6298bbdefa9fc32fdcb5f; munb=2247889693; miid=8009944071033430823; _cc_=UtASsssmfA%3D%3D; mt=ci=0_0; enc=APoYVX5o4cdB1lljqte5WpXepJlCgvvUWIYTkKYb03IcVBmUCSUBlQmYJrw3hnbSAZgtDhbBPKLdNvTNjQeGKw%3D%3D; cookie2=1c8f32a6a72777044e8fa7ce4103cb72; _tb_token_=59036313efb3e; JSESSIONID=04DCADE7E9152973A01A1180586F4EFC; x=761383686; uc1=cookie14=UoTeOL8el8F8eA%3D%3D&lng=zh_CN; uc3=nk2=&id2=&lg2=; tracknick=; sn=%E4%B8%89%E6%B4%8B%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%95%B0%E6%8D%AE%E7%BB%84; csg=210a608b; unb=3789122802; skt=d713088cee404893; _euacm_ac_l_uid_=3789122802; 3789122802_euacm_ac_c_uid_=761383686; 3789122802_euacm_ac_rs_uid_=761383686; _euacm_ac_rs_sid_=68898854; _portal_version_=new; v=0; isg=BNvb6ttpBZxekXn30fc-h2UDajnpr4wxx9MfeM0Y91rxrPqOVYEzAnetQgwijEeq',
    },
}


# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
    # 'Referer': 'https://sycm.taobao.com/mq/industry/product/rank.htm',
# #   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# #   'Accept-Language': 'en',
# #     'Cookie': 't=09d0a59e21c3059e1be220c847b71b0a; cna=Wa9VE42Yoi8CAXARX/Mk4npp; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=162d2ee4cd2a11-01ca86c68c73d1-33697b04-1fa400-162d2ee4cd3dbb; tg=0; l=AvPzoxfP85MORwVh2x7lo1UGA/wdQIfq; ali_ab=112.17.95.243.1524795971924.1; _cc_=WqG3DMC9EA%3D%3D; enc=xAkyqygfceWeolvrC4RuKbh5VGtyafIoA99k6lZ%2FMAQzg%2BDvZ9kjQMu9XxoF8R86MsaXTjainFChDzL0Vl1quQ%3D%3D; mt=ci=0_0; cookie2=194049c4cf6fe3e633601f61857c8932; _tb_token_=e3b3e7553e536; x=2973966816; uc3=nk2=&id2=&lg2=; tracknick=; sn=%E7%BE%8E%E7%9A%84%E7%94%9F%E6%B4%BB%E7%94%B5%E5%99%A8%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%92%9F%E5%A3%B0; unb=3926989410; JSESSIONID=0FEB3990ECDE344D2AFBE394A91DC753; uc1=cookie14=UoTeO8WGGU%2FEDA%3D%3D&lng=zh_CN; csg=3f0ad262; skt=5921ff19a69bee26; v=0; _euacm_ac_rs_sid_=286653957; apushdca7b9c682ea9ac583b99c7b9c86ccd8=%7B%22ts%22%3A1525844671715%2C%22heir%22%3A1525844664582%2C%22parentId%22%3A1525835132935%7D; isg=BJ6eKFT4SDuuLJxMFCijXIgE7zJMQAFaYTq-dkgnzeFfaz1FsO5Y6HuNZ3fn01rx',
#     'Cookie': 't=09d0a59e21c3059e1be220c847b71b0a; cna=Wa9VE42Yoi8CAXARX/Mk4npp; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=162d2ee4cd2a11-01ca86c68c73d1-33697b04-1fa400-162d2ee4cd3dbb; tg=0; l=AvPzoxfP85MORwVh2x7lo1UGA/wdQIfq; ali_ab=112.17.95.243.1524795971924.1; mt=ci=0_0; enc=r0zlCaLneLKN7ZYEQ7cd7z5GrtHhiMhZKcoKX8iSqalQ9v1FrcWp%2F0rBBIOZ6sQV3X8V3NzGmhS79%2FxoWNe0HQ%3D%3D; cookie2=1d9bfe899eae60e3efa5f37f02f8973e; _tb_token_=eee5af35b63d6; _m_h5_tk=ee2612c47c08f08d6ffc86dc0594753d_1526283678874; _m_h5_tk_enc=966ec13cf4d6298bbdefa9fc32fdcb5f; munb=2247889693; _cc_=UIHiLt3xSw%3D%3D; x=2973966816; JSESSIONID=F4E7F68214F885C8404E45FD35DDD189; uc1=cookie14=UoTeOL0pskiWsQ%3D%3D&lng=zh_CN; uc3=nk2=&id2=&lg2=; tracknick=; sn=%E7%BE%8E%E7%9A%84%E7%94%9F%E6%B4%BB%E7%94%B5%E5%99%A8%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%92%9F%E5%A3%B0; csg=7d12d6b0; unb=3926989410; skt=a3fdf085b0f1e6a1; _euacm_ac_l_uid_=3926989410; 3926989410_euacm_ac_c_uid_=2973966816; 3926989410_euacm_ac_rs_uid_=2973966816; _euacm_ac_rs_sid_=286653957; _portal_version_=new; v=0; isg=BCAgm0ogbpjWQNKGJp4FJvpa8SheNmdwMxTwPJox8TvOlcG_Qjm2giIkKT0VJbzL',
# #     'Cookie': 't=09d0a59e21c3059e1be220c847b71b0a; cna=Wa9VE42Yoi8CAXARX/Mk4npp; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=162d2ee4cd2a11-01ca86c68c73d1-33697b04-1fa400-162d2ee4cd3dbb; tg=0; l=AvPzoxfP85MORwVh2x7lo1UGA/wdQIfq; ali_ab=112.17.95.243.1524795971924.1; _cc_=WqG3DMC9EA%3D%3D; enc=xAkyqygfceWeolvrC4RuKbh5VGtyafIoA99k6lZ%2FMAQzg%2BDvZ9kjQMu9XxoF8R86MsaXTjainFChDzL0Vl1quQ%3D%3D; mt=ci=0_0; cookie2=194049c4cf6fe3e633601f61857c8932; _tb_token_=e3b3e7553e536; x=2973966816; uc3=nk2=&id2=&lg2=; tracknick=; sn=%E7%BE%8E%E7%9A%84%E7%94%9F%E6%B4%BB%E7%94%B5%E5%99%A8%E6%97%97%E8%88%B0%E5%BA%97%3A%E9%92%9F%E5%A3%B0; unb=3926989410; JSESSIONID=25CAB83EFFD3D40EA81A451D7405EAC5; uc1=cookie14=UoTeO8R7X6skWg%3D%3D&lng=zh_CN; csg=1e9a2826; skt=8cd0427c556cb14f; v=0; _euacm_ac_rs_sid_=286653957; apushdca7b9c682ea9ac583b99c7b9c86ccd8=%7B%22ts%22%3A1525916523349%2C%22heir%22%3A1525852329210%2C%22parentId%22%3A1525844664582%7D; isg=BPT0LewCEtSpjYaKUvqpYjY2xbTK0ns0z-gEMI5VCH8C-ZZDttzARlw_fTEhAVAP',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Sycm.middlewares.SycmSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Sycm.middlewares.SycmDownloaderMiddleware': 543,
   # 'Sycm.middlewares.CookieMiddleware': 443,
   'Sycm.middlewares.UserAgentMiddleware': 543,
   'Sycm.middlewares.ProxyMiddleware': 443,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
   # 'Sycm.pipelines.SycmPipeline': 300,
   # 'Sycm.pipelines.SycmAllPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
