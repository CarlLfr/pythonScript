import re, os
import time, datetime, locale
import requests
# import schedule
from bs4 import BeautifulSoup
# from wxpy import *
from get_proxies_ip import proxies_ip
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GetEarlyNewsAndSendToWechart(object):
    '''
    获取泡面小镇-泡面早报
    '''

    def __init__(self):
        self.base_url = 'https://www.pmtown.com'
        self.early_news_home_url = 'https://www.pmtown.com/archives/category/%e6%97%a9%e6%8a%a5'
        # self.bot = Bot()    # 登录微信，第一次需要扫码，可以缓存，不用每次登录
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        }
        self.proxies = {"http": "{}".format(proxies_ip())}


    def get_news_url(self):
        '''获取当天早报地址，与页面最新新闻的时间'''
        resp = requests.get(url=self.early_news_home_url, headers=self.headers, proxies=self.proxies, verify=False)
        resp.encoding = 'utf-8'

        resp = str(resp.text)
        # print(resp)
        url_pat = '<a href="(.*?)" target="_blank"'
        date_pat = '>#泡面早班车#(.*?)  星期'
        result1 = re.compile(url_pat).search(resp)
        result2 = re.compile(date_pat).search(resp)
        news_url = result1.groups()[0]
        latest_date = result2.groups()[0].strip()
        # print(news_url)
        # print(latest_date)
        return news_url, latest_date

    def get_current_date(self):
        '''获取当天日期'''
        # now_time = datetime.datetime.now()
        # str_time = now_time.strftime('%Y-%m-%d')
        # locale.setlocale(locale.LC_CTYPE, 'chinese')
        # str_time = time.strftime('%Y年%m月%d日')
        year = datetime.datetime.now().year
        mon = datetime.datetime.now().month
        day = datetime.datetime.now().day
        str_date = str(year) + "年" + str(mon) + "月" + str(day) + "日"
        return str_date

    def write_news_to_text(self, m, news):
        '''写入text文件'''
        text_path = self.base_path + '/news.txt'
        with open(text_path, m, encoding='utf-8') as f:
            f.writelines(news + ' \r\n')

    def get_news(self, news_url):
        '''请求当天早报地址，获取早报内容'''
        url = news_url
        resp = requests.get(url=url, headers=self.headers, proxies=self.proxies, verify=False)
        resp.encoding = 'utr-8'
        html = resp.text

        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        html_str = str(soup.find('div', 'post-content'))    # 新闻内容在<div class="post-content">下
        text = re.sub(r'<.*?>', '', html_str)   # 去掉html_str的html标签
        # print(text)
        return text

    def write_news_to_file(self):
        '''将新闻写入文件，判断是否有今天的新闻'''
        # 判断是否有当天新闻
        news_url, latest_date = self.get_news_url()
        current_date = self.get_current_date()
        news = self.get_news(news_url)
        # print(news)
        if current_date == latest_date:
            news_str = news
        else:
            news_str = "未获取到今天的新闻！！！"
        self.write_news_to_text("w", news_str)



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


if __name__ == '__main__':
    gan = GetEarlyNewsAndSendToWechart()
    # print(gan.get_current_date())
    # gan.get_news_url()
    # print(gan.get_news())
    gan.write_news_to_file()