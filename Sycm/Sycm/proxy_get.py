import requests
import xlsxwriter

from utils.format_style import xlsx_style


def ip_port():
    resp = requests.get('http://47.100.236.184/random')
    proxy_ip, proxy_port = resp.text.split(':')
    return proxy_ip, proxy_port


class TestExcel(object):
    colname = [
        '月份',
        '品牌名称',
        'Haier/海尔',
        'SIEMENS/西门子',
        'Midea/美的',
        'Samsung/三星',
        'Bosch/博世',
        'Whirlpool/惠而浦',
        'Royalstar/荣事达',
        'DIQUA/帝度',
    ]

    rowname = [
        '支付商品数',
        '支付转化率',
        '客单价',
        '访客数',
        '收藏人数',
        '加购人数',
    ]
    def __init__(self):
        # 创建一个新的excel文件并添加一个工作表
        self.wb = xlsxwriter.Workbook('test.xlsx')
        # 创建工作簿
        self.ws = self.wb.add_worksheet('冰箱品牌数据月')
        print('chuang jian trend')

        self.center_style = self.wb.add_format(xlsx_style())

        # 行，列初始值
        self.row = 0
        self.col = 0

        # row_n = 1

        # 设置表头
        for coln in self.colname:
            self.ws.write(self.row, self.col, coln, self.center_style)
            self.col += 1

        self.row_h = 1

        print(self.col)


    def test_excel(self, item):
        item_dict = dict()
        item_dict['支付商品数'] = item['payItemCnt']
        item_dict['支付转化率'] = item['payRate']
        item_dict['客单价'] = item['payPct']
        item_dict['访客数'] = item['uv']
        item_dict['收藏人数'] = item['favBuyerCnt']
        item_dict['加购人数'] = item['addCartUserCnt']

        # print(item_dict)

        # 整理出item字典中的所有key
        item_keys = list(item_dict.keys())
        # print(item_keys)

        year_month = '%s年%s月' % (item['year'], item['month'])
        self.ws.merge_range(self.row_h, 0, self.row_h + 5, 0, year_month, self.center_style)
        # item['']
        if 'Haier/海尔' == item['brand']:
            print(item['brand'])
            self.ws.write(self.row_h, 0, year_month, self.center_style)
            for rown in self.rowname:
                self.ws.write(self.row_h, 1, rown, self.center_style)
                # for item_key in item_keys:
                #     if item_key == rown:
                self.ws.write(self.row_h, 2, item_dict[item_keys[item_keys.index(rown)]], self.center_style)
                self.row_h += 1
                print(self.row_h)



            pass
        elif 'SIEMENS/西门子' == item['brand']:
            print(item['brand'])
            pass
        elif 'Midea/美的' == item['brand']:
            print(item['brand'])
            pass
        elif 'Samsung/三星' == item['brand']:
            print(item['brand'])
            pass
        elif 'Bosch/博世' == item['brand']:
            print(item['brand'])
            pass
        elif 'Whirlpool/惠而浦' == item['brand']:
            print(item['brand'])
            pass
        elif 'Royalstar/荣事达' == item['brand']:
            print(item['brand'])
            pass
        elif 'DIQUA/帝度' == item['brand']:
            print(item['brand'])
            pass
        # else:
        #     self.wb.close()



        # ws.write()
        # pass

    def __del__(self):
        self.wb.close()


# if __name__ == '__main__':
    # test_excel()
item_list = [
    {
        'brand': 'Haier/海尔',
        'cate': 'fridge',
        'mark': 'brand',
        'year': 2017,
        'month': 2,
        'payItemCnt': 1,
        'payPct': 1,
        'payRate': 1,
        'uv': 1,
        'favBuyerCnt': 1,
        'addCartUserCnt': 1,
    },
    {
        'brand': 'Haier/海尔',
        'cate': 'fridge',
        'mark': 'brand',
        'year': 2017,
        'month': 3,
        'payItemCnt': 2,
        'payPct': 2,
        'payRate': 2,
        'uv': 2,
        'favBuyerCnt': 2,
        'addCartUserCnt': 2,
    },
    {
        'brand': 'SIEMENS/西门子',
        'cate': 'fridge',
        'mark': 'brand',
        'year': 2017,
        'month': 2,
        'payItemCnt': 3,
        'payPct': 3,
        'payRate': 3,
        'uv': 3,
        'favBuyerCnt': 3,
        'addCartUserCnt': 3,
    },
    {
        'brand': 'SIEMENS/西门子',
        'cate': 'fridge',
        'mark': 'brand',
        'year': 2017,
        'month': 3,
        'payItemCnt': 4,
        'payPct': 4,
        'payRate': 4,
        'uv': 4,
        'favBuyerCnt': 4,
        'addCartUserCnt': 4,
    },
    {
        'brand': 'Bosch/博世',
        'cate': 'fridge',
        'mark': 'brand',
        'year': 2017,
        'month': 2,
        'payItemCnt': 5,
        'payPct': 5,
        'payRate': 5,
        'uv': 5,
        'favBuyerCnt': 5,
        'addCartUserCnt': 5,
    },
    {'brand': 1},
]
a = TestExcel()
for item in item_list:
    # a = TestExcel()
    a.test_excel(item)
    # item = {
    #     'brand': 'Haier/海尔',
    #     'cate': 'fridge',
    #     'mark': 'brand',
    #     'year': 2017,
    #     'month': 2,
    #     'payItemCnt': 1,
    #     'payPct': 1,
    #     'payRate': 1,
    #     'uv': 1,
    #     'favBuyerCnt': 1,
    #     'addCartUserCnt': 1,
    # }
    # print(ip_port())

