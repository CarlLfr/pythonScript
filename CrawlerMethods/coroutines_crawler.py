import re, os
import time
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup

class CoroutinesGetEarlyNews(object):
    '''
    异步协程爬取
    '''
    def __init__(self):
        self.base_url = 'https://www.pmtown.com'
        self.early_news_home_url = 'https://www.pmtown.com/archives/category/%e6%97%a9%e6%8a%a5'
        self.base_path = os.path.dirname(os.path.abspath(__file__))

    def news_url_list(self):
        '''获取当天早报地址'''
        resp = requests.get(self.early_news_home_url)
        resp.encoding = 'utf-8'

        resp = str(resp.text)
        url_pat = '<h2 class="entry-title"><a href="(.*?)" rel="bookmark">'
        url_list = re.compile(url_pat).findall(resp)
        news_url_list = [self.base_url + url for url in url_list]
        # print(news_url_list)
        return news_url_list

    # sem = asyncio.Semaphore(10) # 信号量，控制协程数，防止爬的过快

    async def get_news(self, url):
        '''请求当天早报地址，获取早报内容'''
        # with (await sem):
            # async with是异步上下文管理器
        async with aiohttp.ClientSession() as session:  # 获取session
            async with session.get(url) as resp:  # 提出请求
                resp.encoding = 'utr-8'
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')
                html_str = str(soup.find('div', 'single-entry-summary'))  # 新闻内容在<div class="single-entry-summary">下
                text = re.sub(r'<.*?>', '', html_str)  # 去掉html_str的html标签
                self.write_news_to_text("a", text)  # 写入txt文件

    def write_news_to_text(self, m, news):
        '''写入text文件'''
        text_path = self.base_path + '/news.txt'
        with open(text_path, m, encoding='utf-8') as f:
            f.writelines(news + ' \r\n')

    def main(self):
        urls = self.news_url_list()
        loop = asyncio.get_event_loop()           # 获取事件循环
        tasks = [self.get_news(url) for url in urls]  # 把所有任务放到一个列表中
        loop.run_until_complete(asyncio.wait(tasks)) # 激活协程
        loop.close()  # 关闭事件循环


if __name__ == '__main__':
    start_time = time.time()
    CoroutinesGetEarlyNews().main()
    end_time = time.time()
    print("总耗时：{}s".format(float(end_time - start_time)))