import requests
from bs4 import BeautifulSoup
from get_pmtown_early_news import GetEarlyNewsAndSendToWechart

# 中国天气网
# 杭州7天天气：http://www.weather.com.cn/weather/101210101.shtml
# 上海7天天气：http://www.weather.com.cn/weather/101020100.shtml

class GetWeatherForCity(object):
    '''
    获取今天、明天、后天的天气预报
    '''
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }

    def get_weather(self, city, url):
        '''写入城市名、近三天天气预报'''
        gn = GetEarlyNewsAndSendToWechart()
        gn.write_news_to_text("a", city+"近三天天气预报：")

        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf-8'
        html = resp.text
        # print(html)

        soup = BeautifulSoup(html, 'lxml')
        links = soup.select('div[id="7d"] ul li', limit=3)
        # print(links)
        weather_list = []
        for link in links:
            date = link.select('h1')[0].get_text()
            weather = link.select('p[class="wea"]')[0].get_text()
            # temperature_max = link.select('p[class="tem"] span')[0].get_text()
            temperature_min = link.select('p[class="tem"] i')[0].get_text()
            win = link.select('p[class="win"] i')[0].get_text()
            # print(date, weather, temperature_min + "~" + temperature_max + temperature_min[-1], win)
            weather_detail_str = "{}，{}，{} {}，{}".format(
                date, weather, temperature_min, temperature_min[-1], win
            )
            weather_list.append(weather_detail_str)
            gn.write_news_to_text("a", weather_detail_str)

    def cities_weathers(self, weather_url_dic={}):
        '''多个城市的天气'''
        for k, v in weather_url_dic.items():
            self.get_weather(k, v)
        print("天气预报写入完成！")


if __name__ == '__main__':
    cities_dict = {"杭州": "http://www.weather.com.cn/weather/101210101.shtml",
        "上海": "http://www.weather.com.cn/weather/101020100.shtml",
    }
    gw = GetWeatherForCity()
    gw.cities_weathers(cities_dict)
