#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
通过requests模块向文章链接发送get请求，增加博客文章的浏览量
'''

import requests
import random
import time
import threading
import queue
from conf import urlList

class AddPageViewThread(threading.Thread):
    def __init__(self, urlQueue, url_num):
        super(AddPageViewThread, self).__init__()
        self.urlQueue = urlQueue
        self.url_num = url_num
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }

    def run(self):
        while not self.urlQueue.empty():
            url = self.urlQueue.get()
            self.add_page_view(url, self.header, self.url_num)

    def add_page_view(self, url, header, url_num):
        pv1 = random.randint(40, 150)   # 获取前30分钟随机浏览次数
        pv2 = random.randint(300, 2000)    # 获取24小时内随机浏览次数
        print("第{}个链接...前30分钟浏览{}次，24小时内浏览{}次...".format(url_num, pv1, pv2))
        success_time = 1
        fail_time = 1
        while success_time <= pv2:
            try:
                rep = requests.get(url, headers=header)
                if rep.status_code == 200:
                    print("第{}个链接 第{}次浏览成功...".format(url_num, success_time))
                    success_time += 1
                    if success_time <= pv1:
                        time.sleep(random.uniform(5, 10))    # 前30分钟随机暂停
                    else:
                        time.sleep(random.uniform(20, 60))    # 30分钟之后随机暂停
                    continue
            except:
                print("第{}个链接 第{}次浏览失败...".format(url_num, success_time))
                fail_time += 1
                time.sleep(100)
                continue

        print("第{}个链接浏览任务完成，总共浏览了{}次！".format(url_num, success_time - 1))

def main():
    # 线程数
    threads = []
    threadNum = len(urlList)

    # 构造队列
    urlQueue = queue.Queue()
    for url in urlList:
        urlQueue.put(url)

    # 开启threadNum个线程
    for i in range(threadNum):
        url_num = i + 1
        thread = AddPageViewThread(urlQueue, url_num)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
