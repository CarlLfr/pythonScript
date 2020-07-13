from get_weather import GetWeatherForCity
from get_pmtown_early_news import GetEarlyNewsAndSendToWechart

cities_dict = {"杭州": "http://www.weather.com.cn/weather/101210101.shtml",
        "上海": "http://www.weather.com.cn/weather/101020100.shtml",
    }

if __name__ == '__main__':
    # 先写入新闻，再写入天气
    gan = GetEarlyNewsAndSendToWechart()
    gan.write_news_to_file()

    gw = GetWeatherForCity()
    gw.cities_weathers(cities_dict)