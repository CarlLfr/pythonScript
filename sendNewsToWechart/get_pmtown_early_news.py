import re
import os
import time
import requests
# import schedule
from bs4 import BeautifulSoup
# from wxpy import *

class GetEarlyNewsAndSendToWechart(object):
    '''
    获取泡面小镇-泡面早报
    '''

    def __init__(self):
        self.base_url = 'https://www.pmtown.com'
        self.early_news_home_url = 'https://www.pmtown.com/archives/category/%e6%97%a9%e6%8a%a5'
        # self.bot = Bot()    # 登录微信，第一次需要扫码，可以缓存，不用每次登录
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def get_news_url(self):
        '''获取当天早报地址'''
        resp = requests.get(self.early_news_home_url)
        resp.encoding = 'utf-8'

        resp = str(resp.text)
        pat2 = '<h2 class="entry-title"><a href="(.*?)" rel="bookmark">'
        result1 = re.compile(pat2).search(resp)
        news_url = result1.groups()[0]
        return news_url

    def get_news(self):
        '''请求当天早报地址，获取早报内容'''
        url = self.base_url + self.get_news_url()
        resp = requests.get(url)
        resp.encoding = 'utr-8'
        html = resp.text

        soup = BeautifulSoup(html, 'html.parser')
        html_str = str(soup.find('div', 'single-entry-summary'))    # 新闻内容在<div class="single-entry-summary">下
        text = re.sub(r'<.*?>', '', html_str)   # 去掉html_str的html标签
        return text

    # def sent_charRoom_msg(self, bot, name, context):
    #     '''群发送消息'''
    #     my_group = bot.groups().search(name)[0]
    #     my_group.send(context)
    #
    # def send_news(self):
    #     '''发送消息'''
    #     news_text = self.get_news()    # 获取需要发送的新闻
    #     group_list = ["一群大傻逼"]   # 群名，可以多个
    #     for group_name in group_list:
    #         self.sent_charRoom_msg(self.bot, group_name, news_text)
    #         print("向{}发送新闻！".format(group_name))

    # def main(self):
    #     job = self.send_news()
    #     schedule.every().day.at('9:00').do(job)
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)
    #     self.bot.join()

    def write_news_to_text(self):
        '''写入text文件'''
        text_path = self.base_path + '/news.txt'
        news = self.get_news()
        with open(text_path, "w", encoding='utf-8') as f:
            f.writelines(news)


if __name__ == '__main__':
    gan = GetEarlyNewsAndSendToWechart()
    # print(gan.get_news())
    gan.write_news_to_text()