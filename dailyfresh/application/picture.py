from urllib import request
import random
from urllib import parse
from pymysql import *
import gevent
from lxml import etree
from gevent import monkey
import time
import re
# monkey.patch_all()
class Spaider:
    def __init__(self, page, name):
        self.page = page
        self.name = name
        self.list = []
        # self.cnno = connect(host='127.0.0.1', port=3306, database='picture',
        #                user='root', password='mysql', charset='utf8')
        # self.cs1 = self.cnno.cursor()
        # 虽然可以做到并发多协程,但是因为图片的访问需要
        # 访问数据库,如果是同一个数据库的话会造成阻塞,只有一个能访问
        # 所以每一个协程创建一个数据库然后再response完毕之后再删除
        i = str(random.randint(0, 10000000000000000))
        self.str1 = 'picture' + i
        # self.cs1.execute('create table if not exists %s (url VARCHAR (100) not NULL)' % self.str1)
    def start(self):
        # dirct1 = {'word': '%s' % self.name, 'pn': '%s' % str((self.page-1)*10), 'tn': 'baiduimage'}
        dirct1 = {'page': '%s' % str(self.page)}
        url2 = parse.urlencode(dirct1)
        # url1 = 'https://image.baidu.com/search/index?'
        url1 = 'http://www.doutula.com/article/list/?'
        url = url1 + url2
        # self.save_picture(self.get_picture_url(url))
        # g = gevent.spawn(self.save_picture, self.get_picture_url(url))
        # g.join()
        self.save_picture(self.get_picture_url(url))
        return self.list

    def get_picture_url(self,url):
        req = request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        respons = request.urlopen(req)
        html = respons.read().decode()
        html = etree.HTML(html)
        page_urls = html.xpath('//div[@class="col-sm-9"]/a/@href')
        # patter = re.compile(r'"thumbURL":"(.*?)"', re.S | re.I)
        # picture_urls = re.findall(patter, html)
        return page_urls

    def save_picture(self, page_urls):
        for page_url in page_urls:
            req = request.Request(page_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
            respons = request.urlopen(req)
            html = respons.read().decode()
            html = etree.HTML(html)
            picture_urls = html.xpath('//td/a[@href]/img/@src')
            self.list.extend(picture_urls)
            # for picture_url in picture_urls:
            #     self.cs1.execute('insert into %s VALUES(0,\'%s\')' % (self.str1, picture_url))
            #     self.cnno.commit()
if __name__ == '__main__':
    s1 = time.time()
    spider = Spaider(2, 'meinv')
    spider.start()
    # spider.delete_table()
    s2 = time.time()
    print(s2-s1)