#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Usage:
    输入要查询的火车类型可以多选（动车d,高铁g,特快t,快速k,直达z）
    输入出发地、目的地、出发日期。
    查询结果以命令行形式自动呈现。

Examples:
    Please input the trainType you want to search: dgz
    Please input the city you want leave: 南京
    Please input the city you will arrive: 北京
    Please input the data(Example: 2017-09-27): 2019-05-30
"""

import json
import requests
from docopt import docopt
from prettytable import PrettyTable
from colorama import init, Fore
from stations import stations

class SearchTrain(object):
    def __init__(self):
        self.trainOption = input('-d动车 -g高铁 -k快车 -t特快 -z直达, Please input the trainType you want to search:')
        self.fromStation = input('Please input the city you want leave:')
        self.toStation = input('Please input the city you will arrive:')
        self.tripDate = input('Please input the date(Example: 2019-05-30):')
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Cookie": "JSESSIONID=EF9BC5ABCDD7EA1B9D45BDEC3C4C5412; _jc_save_wfdc_flag=dc; BIGipServerotn=401605130.38945.0000; BIGipServerpool_passport=267190794.50215.0000; RAIL_EXPIRATION=1558890528969; RAIL_DEVICEID=QphCK5OaQiEGgTqcKoTZeW-xkoey05RxIe5XUCjvyk_rDmwxvArJTZrjl0iK1rzUk4Xbhy34ahX2QqvP9_0KrcisLgE9KyfWbClYqXGlzrQmIJmo4a9VJTgccTWzqGAaUrBvh2n-8uQITzWqDSeBgdZm-0MsIrGJ; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_fromDate=2019-05-24; _jc_save_toDate=2019-05-23; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH"
        }
        self.available_trains, self.options = self.searchTrain()

    def trains(self):
        for item in self.available_trains:
            data_list = item.split('|')
            train_no = data_list[3]
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + data_list[6] + Fore.RESET,
                               Fore.RED + data_list[7] + Fore.RESET]),
                    '\n'.join([Fore.GREEN + data_list[8] + Fore.RESET,
                               Fore.RED + data_list[9] + Fore.RESET]),
                    data_list[10],
                    data_list[32],
                    data_list[25],
                    data_list[31],
                    data_list[30],
                    data_list[21],
                    data_list[23],
                    data_list[28],
                    data_list[24],
                    data_list[29],
                    data_list[26],
                    data_list[22]
                ]
                yield train

    def pretty_print(self):
        # 创建表格
        pt = PrettyTable()
        # 添加表头
        header = '车次 车站 时间 历时 商务座 特等座 一等 二等 高级软卧 软卧 硬卧 软座 硬座 无座 其他'.split()
        pt._set_field_names(header)
        # 按行添加train内容
        for train in self.trains():
            pt.add_row(train)
        print(pt)

    def searchTrain(self):
        arguments = {
            'option': self.trainOption,
            'from': self.fromStation,
            'to': self.toStation,
            'date': self.tripDate
        }
        options = ''.join([item for item in arguments['option']])
        from_station, to_station, date = stations[arguments['from']], stations[arguments['to']], arguments['date']
        url = ('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={},BJP&ts={},SHH&date={}&flag=N,N,Y').format(from_station, to_station, date)
        requests.packages.urllib3.disable_warnings()
        html = requests.get(url, headers=self.headers, verify=False)
        # requests中response.json()方法等同于json.loads（response.text）方法
        available_trains = html.json()['data']['result']
        return available_trains, options

if __name__ == '__main__':
    while True:
        stn = SearchTrain()
        stn.pretty_print()


