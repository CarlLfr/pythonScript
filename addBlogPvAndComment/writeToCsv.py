#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from conf import *

# 将评论写入csv文件
def writeCommentToCsv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow([row])

# def writeAuthorEmailToCsv(filename, data):
#     with open(filename, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(data)

# 读取文件
def readCsv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        r = list(reader)
    return r

if __name__ == '__main__':
    # data1 = commentList
    # data2 = authorEmailList
    commentFilename = r'F:\blogHits\addBlogPvAndComment\comments.csv'
    authorEmailFilename = r'F:\blogHits\addBlogPvAndComment\authorAndEmail.csv'
    # writeCommentToCsv(commentFilename, data1)
    # print("评论写入成功！")
    # writeCommentToCsv(authorEmailFilename, data2)
    # print("姓名与邮箱写入成功")

    data = readCsv(commentFilename)
    for i in data[0:6]:
        print(i[0])

