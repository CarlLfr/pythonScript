#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import threading
import json
import requests
from jsonpath import jsonpath

class PhotoDonwload(threading.Thread):
    def __init__(self):
        super(PhotoDonwload, self).__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        }
        self.searchName = input("请输入要搜索的图片种类：")

    # 构造http请求的get请求方法
    def getRequest(self, url, header):
        try:
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

    # 新建文件夹
    # def mkdir(self):
    #     path = r'F:\photos\{}'.format(self.searchName)
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     return path

    def get_kinds_photo(self):
        url = 'http://www.bigbigwork.com/board/r?h={}&p=1&r=22'.format(self.searchName)
        result1 = self.getRequest(url, self.headers)
        jsonStr1 = json.loads(result1)
        uidList = jsonpath(jsonStr1, '$..uid')
        bidList = jsonpath(jsonStr1, '$..bid')

        # 根据uid,bid构造搜索结果界面各主题的url
        pul = []
        for i in range(len(uidList)):
            for j in range(1, 10):
                kind_url = 'http://board.bigbigwork.com/img/listBoardImg?user_token=&uid={}&board_id={}&page={}&rows=22&like='.format(uidList[i], bidList[i], j)
                result2 = self.getRequest(kind_url, self.headers)
                jsonStr2 = json.loads(result2)
                photoUrlList = jsonpath(jsonStr2, '$..url')
                if photoUrlList is False:
                    break
                pul.extend(photoUrlList)
        return pul

    # 下载并保存图片
    def download_photo(self):
        photoUrlList = self.get_kinds_photo()
        # filename = self.mkdir()
        filename = r'F:\photos\test_1'
        i = 1
        for url in photoUrlList:
            print("开始下载第%d张图片..." % i)
            result = requests.get(url, headers=self.headers).content
            with open(filename+"\{}.jpg".format(i), 'wb') as f:
                f.write(result)
            i += 1

def main():
    pdl = PhotoDonwload()
    pdl.download_photo()

if __name__ == '__main__':
    main()