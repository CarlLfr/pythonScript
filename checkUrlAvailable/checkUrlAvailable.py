#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import requests

class CheckUrlAvailable(object):
    def __init__(self):
        self.header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
            }

    # 读取原csv文件内容
    def read_csv_info(self, pre_filename):
        with open(pre_filename, 'r') as f:
            reader = csv.reader(f)
            columns = [row for row in reader]
        return columns

    # def get_status_code(columns):
    #     for r in columns:
    #         # 判断是否是标题与空行
    #         if r[0] == '':
    #             pass
    #         else:
    #             if r[1] == '':
    #                 pass
    #             else:
    #                 try:
    #                     rep = requests.get(url=r[1], headers=header)
    #                     statusCode = rep.status_code
    #                     print("请求链接{}，返回状态码为{}...".format(r[1], statusCode))
    #                 except:
    #                     print("链接{}请求不通！".format(r[1]))
    #                     pass
    #     print("筛选完成！")



    def check_available_write_to_csv(self, columns, new_filename):
        # new_filename为筛选过后要写入的新文件路径
        with open(new_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            for r in columns:
                # 判断是否是标题与空行
                if r[0] == '':
                    pass
                else:
                    if r[1] == '':
                        writer.writerow(r)
                    else:
                        try:
                            rep = requests.get(url=r[1], headers=self.header)
                            if rep.status_code == 200:
                                writer.writerow(r)
                            else:
                                print("链接{}请求不通！".format(r[1]))
                        except:
                            print("链接{}请求不通！".format(r[1]))
                            pass
            print("筛选完成！")

if __name__ == '__main__':
    columns = CheckUrlAvailable.read_csv_info()
    CheckUrlAvailable.check_available_write_to_csv(columns)
    # get_status_code(columns)