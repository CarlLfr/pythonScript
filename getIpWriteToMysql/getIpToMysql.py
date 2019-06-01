#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
爬取https://www.xicidaili.com国内高匿代理ip，并存入数据库
思路：通过爬取高匿代理页面源码清洗出ip信息，再将ip信息写入mysql数据库
'''

import requests
import time
import random
import pymysql
from bs4 import BeautifulSoup

class GetIpIntoToMysql():
    def __init__(self):
        self.base_url = "https://www.xicidaili.com/nn/{}"
        self.endPage = 5
        # 连接mysql数据库
        self.mysql_connect = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='work_data', charset='utf8')

    # 请求https://www.xicidaili.com国内高匿代理ip，获取ip信息
    def get_ip_info_to_mysql(self):
        PROXIES = {}
        try_times = 0
        max_change_proxies_times = 100
        # 连接数据库
        cursor = self.mysql_connect.cursor()

        # 获取每页的源码信息
        for i in range(self.endPage):
            HEADERS = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Referer": self.base_url.format(i if i > 0 else ''),
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            }
            url = self.base_url.format(i+1)

            # 循环获取网页的源码
            while True:
                resp = requests.get(url, headers=HEADERS, proxies=PROXIES)
                # 每隔一段时间请求一次，否则ip会被封
                time.sleep(random.uniform(1.5, 4))
                # 如果返回状态码为503（ip被封），则换ip地址
                if resp.status_code == 503:
                    PROXIES = self.get_proxies(cursor)
                    try_times += 1
                    print("正在尝试第%d次请求，当前ip为%s" % (try_times, PROXIES))
                    # 如果尝试次数大于设定的次数则退出函数
                    if try_times > max_change_proxies_times:
                        print("超过最大尝试次数，连接失败！")
                        return -1
                    continue
                else:
                    # 如果返回码是200, 就跳出while循环, 对爬取的页面进行处理
                    break

            # 清洗每页源码中的ip具体信息
            print("正在抓取第{}页的数据...".format(i+1))
            soup = BeautifulSoup(resp.text, 'lxml')
            ip_list = soup.select('table[id="ip_list"] tr')
            for link in ip_list[1:]:
                ip_n = link.select('td')[1].get_text().strip()
                port_n = link.select('td')[2].get_text().strip()
                try:
                    server_detail_n = link.select('td')[3].a.get_text().strip()
                except:
                    server_detail_n = ''
                high_hidden_n = link.select('td')[4].get_text().strip()
                http_kind_n = link.select('td')[5].get_text().strip()
                time_to_live_n = link.select('td')[8].get_text().strip()
                verify_time_n = link.select('td')[9].get_text().strip()

                # 将清洗得到的ip信息写入mysql数据库
                insert_sql = 'INSERT INTO `proxies_ip_info_a`(ip, port_num, http_kind, server_detail, is_high_hidden, time_to_live, verify_time) VALUES(%s, %s, %s, %s, %s, %s, %s);'
                cursor.execute(insert_sql, (ip_n, port_n, http_kind_n, server_detail_n, high_hidden_n, time_to_live_n, verify_time_n))
                self.mysql_connect.commit()
            print("第{}页数据写入数据库完成...".format(i+1))
            time.sleep(random.uniform(1.5, 4))

    # 检验ip是否可用(通过给定的代理ip请求http://www.baidu.com)
    # def checkIpAvailable(self, http_lind, ip, port, test_url='http://www.baidu.com'):
    #     PROXY = {http_lind: ip + ':' + port}
    #     try:
    #         resp = requests.get(url=test_url, proxies=PROXY, timeout=2)
    #         if resp.status_code == 200:
    #             # print("{}检测通过".format(PROXY))
    #             return PROXY
    #     except:
    #         print("{}无效".format(PROXY))

    # 请求时返回状态码为503（ip被封），则换ip地址，此方法为获取数据库已有的ip信息
    def get_proxies(self, cursor):
        insert_sql = 'select http_kind, ip, port_num from proxies_ip_info_a order by id desc limit 100;'
        cursor.execute(insert_sql)
        # 获取全部返回结果
        results = cursor.fetchall()

        # 构造proxies列表，将数据库获取到的ip信息加入列表
        ip_info_list = []
        for row in results:
            http = row[0]
            ip = row[1]
            port = row[2]
            ip_info = {http: ip + ":" + port}
            ip_info_list.append(ip_info)

        # 在ip_info_list列表中随机获取ip
        ip_proxy = random.choice(ip_info_list)
        return ip_proxy

if __name__ == '__main__':
    ipInfo = GetIpIntoToMysql()
    ipInfo.get_ip_info_to_mysql()