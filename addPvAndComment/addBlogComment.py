#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
评论的内容、姓名、邮箱作为参数，发送接口请求自动评论博客
'''

import time
import requests
import random
import threading
import queue
from bs4 import BeautifulSoup
from conf import *

# 获取文章网页源代码中关于POST_ID的标签，再进行数据清洗获取文章post_id
def get_post_id():
    postIdList = []
    try:
        for url in urlList:
            html = requests.get(url, headers=header).text
            soup = BeautifulSoup(html, 'lxml')
            post_id = soup.find('input', type="hidden")['value']
            postId = int(post_id)   # 清洗出来的post_id为str，转换成int
            postIdList.append(postId)
    except:
        print("获取post_id失败！")

    return postIdList

# 定义评论线程
class AddCommentsThread(threading.Thread):
    def __init__(self, postIdQueue):
        super(AddCommentsThread, self).__init__()
        self.postIdQueue = postIdQueue

    # 获取评论内容，通过设置变量judge来判断是否获取第一条评论的内容
    def get_comment(self, judge):
        if judge == 1:
            comment = random.choice(first_commentList)
        else:
            comment = random.choice(commentList)
        return comment

    # 获取姓名、邮箱
    def get_author_email(self):
        author = random.choice(authorEmailList)[0]
        email = random.choice(authorEmailList)[1]
        return author, email

    # 发送参数请求评论接口
    def add_comment(self, post_id):
        comment_times1 = random.randint(6, 20) # 30分钟之内10条评论
        comment_times2 = random.randint(25, 60) # 24小时内20条评论
        print("POST_ID为{}的文章 30分钟之内评论次数设定为{}，24小时之内评论次数设定为{}...".format(post_id, comment_times1, comment_times2))
        success_times = 1
        fail_times = 1

        while success_times <= comment_times2:
            try:
                # 判断是否是第一条评论
                if success_times == 1:
                    judge = 1
                    comment = self.get_comment(judge)
                else:
                    judge = 0
                    comment = self.get_comment(judge)

                author, email = self.get_author_email()
                form_data = {
                    "comment": comment,
                    "author": author,
                    "email": email,
                    "url": "",
                    "submit": submit,
                    "comment_post_ID": post_id,
                    "comment_parent": comment_parent,
                }

                rep = requests.post(url=comment_url, headers=header, data=form_data)
                print("POST_ID为{}的文章 第{}次评论成功，评论作者是：{}，评论内容为：{}...".format(post_id, success_times, author, comment))
                if success_times <= comment_times1:
                    time.sleep(random.uniform(300, 600))
                else:
                    time.sleep(random.uniform(3456, 1440))
                success_times += 1
                continue
            except Exception as e:
                print("POST_ID为{}的文章 第{}次评论失败，失败原因为：{}".format(post_id, fail_times, e))
                fail_times += 1
                time.sleep(2)
                if fail_times < 10:
                    continue
                else:
                    break

        print("POST_ID为{}的文章评论任务完成，总共评论了{}次！".format(post_id, success_times - 1))

    def run(self):
        while not self.postIdQueue.empty():
            post_id = self.postIdQueue.get()
            self.add_comment(post_id)

def main():
    # 根据文章数构造线程数
    threads = []
    threadNum = len(urlList)

    # 构造post_id队列
    postIdQueue = queue.Queue()
    postIdList = get_post_id()
    for post_id in postIdList:
        postIdQueue.put(post_id)

    # 开启threadNum个线程
    for i in range(threadNum):
        thread = AddCommentsThread(postIdQueue)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()