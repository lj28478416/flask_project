from urllib import request
from lxml import etree
from pymysql import *
import re
class Ticket:
    def __init__(self,station_info):
        self.station_info = station_info
    # 更新数据库中的数据表
    def update_database(self):
        url = 'http://www.tieyou.com/newlist_js.php'
        req = request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
        html = request.urlopen(req).read().decode('gbk')
        from_station_num = re.findall(r'\'(.+?)\'\,\s\'[\w]+?\'\,\s\'(.+?)\'', html)
        print(from_station_num)
        cnno = connect(host='127.0.0.1',port=3306,database = 'ticket',user = 'root',password = 'mysql',charset='utf8')
        cs1 = cnno.cursor()
        cs1.execute('drop table ticket')
        cs1.execute('create table if not EXISTS ticket(id int auto_increment PRIMARY KEY,name VARCHAR(20) not NULL , name_en VARCHAR(20) not null)')
        for i in from_station_num:
            sql= 'insert into ticket VALUES(default,%s,%s)'
            cs1.execute(sql, [i[0], i[1]])
        cnno.commit()
    # 获取火车票信息
    def ticket_informatin(self):
        url = 'http://www.tieyou.com/daigou/%s-%s.html?date=%s&utm_source=tieyou&is_local=1' % ( self.station_info[0], self.station_info[1], self.station_info[2])
        req = request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
        html1 = request.urlopen(req).read().decode('gbk')
        html = etree.HTML(html1)
        train_num_list = html.xpath('//ul/@trainname')
        train_information = {}

        for train_num in train_num_list:
            train_num = '\"' + train_num +'\"'
            train_information_list = []
            # 出发时间
            from_time = html.xpath('// ul[@ trainname=%s] / li[1] / strong / text()' % train_num)
            train_information_list.extend(from_time)
            # # 到站时间
            to_time = html.xpath('// ul[@ trainname=%s] / li[1] / span / text()' % train_num)
            train_information_list.extend(to_time)
            # 历时
            time = html.xpath('// ul[@ trainname=%s] / li[4] / text()' % train_num)
            time = re.sub(r'\s', '', time[0])
            train_information_list.append(time)
            # 车票
            ticket = html.xpath('// ul[@ trainname=%s] / li[5]' % train_num)
            ticket = ticket[0].xpath('string(.)')
            ticket = re.sub(r'\s', '', ticket)
            train_information_list.append(ticket)
            train_information[train_num] = train_information_list
        return train_information

if __name__ == '__main__':
    train_date = '1'
    from_station = '2'
    to_station = '3'
    ticket = Ticket('aaa')
    ticket.update_database()