from urllib import request
from lxml import etree
import time
class GuichuVideo:
    def __init__(self):
        pass
    def start(self):
        # 规定鬼畜视频日期
        page = 1
        if time.localtime().tm_mon < 10 :
            mon = '0' + str(time.localtime().tm_mon)
        else:
            mon = time.localtime().tm_mon
        if time.localtime().tm_mday < 10 :
            day = '0' + str(time.localtime().tm_mday)
        else:
            day = time.localtime().tm_mday
        date1 = '%s-%s-01' % (time.localtime().tm_year,mon)
        date2 = '%s-%s-%s' % (time.localtime().tm_year,mon,day)
        url = "https://www.bilibili.com/v/kichiku/guide/?#/all/click/0/%s/%s,%s" % (page,date1,date2)
        req = request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36')
        html1 = request.urlopen(req).read().decode()
        print(html1)
        html = etree.HTML(html1)
        train_num_list = html.xpath('//li[@class]/div[@class="l-item"]/div[@class="r"]/a/@href')
        print(train_num_list)
if __name__ == '__main__':
    guichuvideo = GuichuVideo()
    guichuvideo.start()