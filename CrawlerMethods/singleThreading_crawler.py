import re, os
import time
import requests
from bs4 import BeautifulSoup

class GetEarlyNews(object):
    '''
    获取泡面小镇-泡面早报
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
        news_url_list = re.compile(url_pat).findall(resp)
        # print(news_url)
        return news_url_list

    def get_news(self, news_url):
        '''请求当天早报地址，获取早报内容'''
        url = self.base_url + news_url
        resp = requests.get(url)
        resp.encoding = 'utr-8'
        html = resp.text

        soup = BeautifulSoup(html, 'html.parser')
        html_str = str(soup.find('div', 'single-entry-summary'))  # 新闻内容在<div class="single-entry-summary">下
        text = re.sub(r'<.*?>', '', html_str)  # 去掉html_str的html标签
        return text

    def write_news_to_text(self, m, news):
        '''写入text文件'''
        text_path = self.base_path + '/news.txt'
        with open(text_path, m, encoding='utf-8') as f:
            f.writelines(news + ' \r\n')

    def main(self):
        news_url_list = self.news_url_list()
        for url in news_url_list:
            news_text = self.get_news(url)
            self.write_news_to_text("a", news_text)


if __name__ == '__main__':
    start_time = time.time()
    ge = GetEarlyNews()
    ge.main()
    end_time = time.time()
    print("总耗时：{}s".format(float(end_time-start_time)))