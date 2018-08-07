from selenium import webdriver
import openpyxl
import jieba
from bs4 import BeautifulSoup
import time
# import jieba
import os
import re
import chardet
import random
from PyQt5 import QtCore, QtGui, QtWidgets

from Sycm.settings import MY_USER_AGENT_PC

jieba.set_dictionary("dict/dict.txt")
# jieba.set_dictionary()
jieba.initialize()

# ua列表
# MY_USER_AGENT_PC = [
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
#     'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
# ]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(725, 590)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 411, 471))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(479, 50, 171, 61))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 51, 31))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(430, 480, 80, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(480, 140, 171, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(480, 220, 171, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 725, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "采集"))
        self.label.setText(_translate("MainWindow", "标题："))
        self.pushButton_2.setText(_translate("MainWindow", "清空"))
        self.pushButton_3.setText(_translate("MainWindow", "导出词频"))
        self.pushButton_4.setText(_translate("MainWindow", "启动浏览器"))
        self.menu.setTitle(_translate("MainWindow", "菜单"))
        self.action.setText(_translate("MainWindow", "退出"))

def cutword(data):
    result=jieba.cut(data,cut_all=False)
    return result

def wordfrequency(text):
    sub_re=r'[a-zA-Z]+|[\s+\.\!\/_,$%^*\(\d+\"\']+|[+—；—！:\(\)：《》，。？、~@#￥%……&*（）％～\[\]\|\?\·【】“”;-]+'
    text=re.sub(sub_re,' ',text)
    result={}
    words=[word for word in cutword(text)]
    for word in words:
        if word=='' or word==' ':
            continue
        try:
            result[word]+=1
        except:
            result[word]=1
    return result

class Sycm(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Sycm,self).__init__()
        self.setupUi(self)
        self.titles=[]
        self.basic_init()

    def basic_init(self):
        self.action.triggered.connect(self.close)
        self.pushButton.clicked.connect(self.crawl)
        self.pushButton_3.clicked.connect(self.save_to_excel)
        self.pushButton_2.clicked.connect(self.clear_list)
        self.pushButton_4.clicked.connect(self.getBrowser)

    def message(self,text=''):
        box=QtWidgets.QMessageBox.question(self,"提示",text,QtWidgets.QMessageBox.Ok)
        if box==QtWidgets.QMessageBox.Ok:
            return True
        else:
            return False

    def getBrowser(self):
        self.browser=webdriver.Firefox()
        # self.browser=webdriver.Chrome()
        self.browser.get('https://sycm.taobao.com/custom/login.htm')
        # self.browser.get('https://www.baidu.com')
        self.browser.implicitly_wait(10)
        self.message(text='请在浏览器中登录')

    def save_to_excel(self):
        timenow=time.strftime("%Y%m%d_%H%M%S",time.localtime())
        text=''
        for title in self.titles:
            text+=title
        words=wordfrequency(text)
        result=sorted(words.items(),key=lambda x:x[1],reverse=True)
        excel=openpyxl.Workbook(write_only=True)
        sheet=excel.create_sheet()
        for item in result:
            sheet.append(item)
        try:
            os.mkdir('result')
        except:
            pass
        excel.save('result/%s.xlsx'%timenow)

    def list_show(self):
        self.listWidget.clear()
        for title in self.titles:
            self.listWidget.addItem(title)

    def clear_list(self):
        self.titles.clear()
        self.list_show()

    def crawl(self):
        current_url=self.browser.current_url
        print(current_url)
        cookie = self.browser.get_cookies()
        print(cookie)
        cookie_list = ['%s=%s' % (cookie_dict['name'], cookie_dict['value']) for cookie_dict in cookie]
        cookie_str = '; '.join(cookie_list)
        print(cookie_str)
        headers = {
            'User-Agent': random.choice(MY_USER_AGENT_PC),
            'Cookie': cookie_str,
        }
        # for cookie_dict in cookie:
        #     cookie_nv = '%s=%s; ' % (cookie_dict['name'], cookie_dict['value'])
        #     cookie_str += cookie_nv


            # pass

        # 品牌详情 https://sycm.taobao.com/mq/industry/brand/detail.htm?spm=a21ag.7749233.0.0.1704471096fdjr#/?brandId=10728&cateId=350301&dateRange=2018-06-12%7C2018-06-12&dateType=recent1&device=0&seller=-1
        # https://sycm.taobao.com/mq/brandDetail/getSummary.json?brandId=10728&cateId=350301&dateRange=2018-06-06|2018-06-12&dateType=recent7&device=0&seller=-1&token=8f7cc28b4&_=1528877314176

        if 'industry/brand' in current_url:

            from scrapy import cmdline
            cmd_py = 'scrapy crawl sanyo -a category=%s' % cookie_str
            cmdline.execute(cmd_py.split())
            
            # self.browser.get('https://sycm.taobao.com/mq/brandDetail/getSummary.json?brandId=10728&cateId=350301&dateRange=2018-06-06|2018-06-12&dateType=recent7&device=0&seller=-1&token=8f7cc28b4&_=1528877314176')
            # print(self.browser.page_source)
            pass

        # 行业直播 https://sycm.taobao.com/mq/live/live.htm?spm=a21ag.7749227.LeftMenu.d283.5c5d140dDmpxHg#/?cateId=350301&device=0
        # https://sycm.taobao.com/ipoll/live/industry/showTopItems.json?cateId=350301&cateLevel=2&device=0&limit=100&page=2&seller=-1&size=10&token=8f7cc28b4&_=1528877465494
        elif 'live/live' in current_url:
            self.browser.get('https://sycm.taobao.com/ipoll/live/industry/showTopItems.json?cateId=350301&cateLevel=2&device=0&limit=100&page=2&seller=-1&size=10&token=8f7cc28b4&_=1528877465494')
            print(self.browser.page_source)
            pass


        # 行业大盘 https://sycm.taobao.com/mq/industry/overview/overview.htm?spm=a21ag.7782695.LeftMenu.d293.6758465340eN25#/?cateId=350301&dateRange=2018-06-12%7C2018-06-12&dateType=recent1&device=0&seller=-1
        # https://sycm.taobao.com/mq/overview/reportIndex.json?cateId=350301&dateRange=2018-06-06|2018-06-12&dateType=recent7&device=0&indexCode=uv|searchUvCnt|searchClkRate|favBuyerCnt|addCartBuyerCnt|payPct|payItemQty&seller=-1&token=8f7cc28b4&_=1528877536552

        elif 'industry/overview/overview' in current_url:
            self.browser.get('https://sycm.taobao.com/mq/overview/reportIndex.json?cateId=350301&dateRange=2018-06-06|2018-06-12&dateType=recent7&device=0&indexCode=uv|searchUvCnt|searchClkRate|favBuyerCnt|addCartBuyerCnt|payPct|payItemQty&seller=-1&token=8f7cc28b4&_=1528877536552')
            print(self.browser.page_source)
            pass

        # if 'rankTabIndex' in current_url:
        #     current_url=current_url.replace('&rankTabIndex=0','').replace('&rankTabIndex=1','')
        #     print('change:', current_url)
        # result=[]
        # for num in range(2):
        #     items=[]
        #     self.browser.get(current_url+'&rankTabIndex='+str(num))
        #     time.sleep(2)
        #     try:
        #         items+=self.parser(self.browser.page_source)
        #     except:
        #         self.message(text='解析错误')
        #         return
        #     page=2
        #     while True:
        #         url=current_url+'&rankTabIndex='+str(num)+'&page='+str(page)
        #         self.browser.get(url)
        #         time.sleep(3)
        #         try:
        #             items+=self.parser(self.browser.page_source)
        #         except:
        #             self.message(text='解析错误')
        #             return
        #         page+=1
        #         if page==8:
        #             break
        #     result+=items[:100]
        # self.titles+=result
        # self.list_show()

    def parser(self,html):
        table=BeautifulSoup(html,'lxml').find('table',{'class':['table-ng','table-ng-basic']}).find_all('tr')
        result=[]
        for tr in table:
            try:
                result.append(tr.find('img').get('alt'))
            except:
                continue
        return result


if __name__=='__main__':
    import sys
    app=QtWidgets.QApplication(sys.argv)
    management=Sycm()
    management.show()
    sys.exit(app.exec_())
