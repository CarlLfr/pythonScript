#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import pymysql
from bs4 import BeautifulSoup

class WeatherQuery():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        # 链接数据库
        self.CONNECTION = pymysql.connect(host='localhost', user='root', password='123456', db='test',charset='utf8')

    # 查询数据库获取cityCode
    def getCityCode(self, cityName):
        SQL = "SELECT cityCode from cityWeather WHERE cityName='%s'" % cityName
        try:
            # 使用cursor()方法创建游标对象
            with self.CONNECTION.cursor() as cursor:
                # 执行sql语句
                cursor.execute(SQL)
                # 提交数据
                self.CONNECTION.commit()
                # 获取查询结果
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            print(repr(e))

    def getWeather(self, cityCode, cityName):
        url = 'http://www.weather.com.cn/weather/{}.shtml'.format(cityCode)
        html = requests.get(url, headers=self.headers).content.decode("utf-8","ignore")
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        links = soup.select('div[id="7d"] ul li')
        print("日期   天气  温度  风力")
        for link in links:
            date = link.select('h1')[0].get_text()
            weather = link.select('p[class="wea"]')[0].get_text()
            temperature_max = link.select('p[class="tem"] span')[0].get_text()
            temperature_min = link.select('p[class="tem"] i')[0].get_text()
            win = link.select('p[class="win"] i')[0].get_text()
            print(date, weather, temperature_min+"~"+temperature_max+temperature_min[-1], win)

def main():
    cityName = input("请输入要查询的城市名称：")
    weather = WeatherQuery()
    cityCode = weather.getCityCode(cityName)
    weather.getWeather(cityCode, cityName)

if __name__ == '__main__':
    main()


