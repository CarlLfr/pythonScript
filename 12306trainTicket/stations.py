#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import requests
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
# requests请求时为避免ssl认证，可将verify=False,但这样日志中会有大量的warning信息，
# 此时需加上下面这行代码就能去掉这些报错信息
requests.packages.urllib3.disable_warnings()
html = requests.get(url, verify=False).text
pat = re.compile(r'([\u4e00-\u9fa5]+)\|([A-Z]+)')
station = pat.findall(html)
# print(station)
stations = dict(station)
pprint(stations, indent=4)