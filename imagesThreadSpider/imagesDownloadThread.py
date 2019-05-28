#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import threading
import queue
import json
import requests
from jsonpath import jsonpath

# 获取图片url并加入列表
class GetImagesUrl(object):
    def __init__(self):
        super(GetImagesUrl, self).__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        }
        self.searchName = "建筑设计"

    # 构造http请求的get请求方法
    def getRequest(self, url, header):
        try:
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

    def get_kinds_photo(self):
        url = 'http://www.bigbigwork.com/board/r?h={}&p=1&r=22'.format(self.searchName)
        result1 = self.getRequest(url, self.headers)
        jsonStr1 = json.loads(result1)
        uidList = jsonpath(jsonStr1, '$..uid')
        bidList = jsonpath(jsonStr1, '$..bid')

        print(uidList)
        print(bidList)

        # 根据uid,bid构造搜索结果界面各主题的url
        pul = []
        try:
            for i in range(len(uidList)):
                for j in range(1, 10):
                    kind_url = 'http://board.bigbigwork.com/img/listBoardImg?user_token=&uid={}&board_id={}&page={}&rows=22&like='.format(
                        uidList[i], bidList[i], j)
                    result2 = self.getRequest(kind_url, self.headers)
                    jsonStr2 = json.loads(result2)
                    photoUrlList = jsonpath(jsonStr2, '$..url')
                    if photoUrlList is False:
                        break
                    pul.extend(photoUrlList)
        except Exception as e:
            print(e)
        return pul

# 下载并保存图片线程
class DownloadImagesThread(threading.Thread):
    def __init__(self, urlQueue, fileNum):
        super(DownloadImagesThread, self).__init__()
        self.urlQueue = urlQueue
        self.fileNum = fileNum
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        }

    # 构造run方法
    def run(self):
        imageNum = 1
        filename = self.mkdir()
        while not self.urlQueue.empty():
            url = self.urlQueue.get()
            print("开始下载第%d张图片,并保存到%s文件夹..." % (imageNum, filename))
            self.get_save_image(filename, url, imageNum)
            imageNum += 1
        print("下载完毕！")

    # 下载图片并保存的方法
    def get_save_image(self, filename, url, imageNum):
        try:
            result = requests.get(url, headers=self.headers).content
            with open(filename + "\{}.jpg".format(imageNum), 'wb') as f:
                f.write(result)
        except Exception as e:
            print(e)

    # 新建文件夹
    def mkdir(self):
        path = r'F:\photos\test_{}'.format(self.fileNum)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

def main():
    # 线程数
    threads = []
    threadNum = 3

    # 构造队列
    listQueue = queue.Queue()
    urlList = GetImagesUrl().get_kinds_photo()
    for url in urlList:
        listQueue.put(url)

    # 开启3个线程
    for fileNum in range(threadNum):
        thread = DownloadImagesThread(listQueue, fileNum)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()