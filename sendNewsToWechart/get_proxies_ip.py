import re
import requests
import random

def proxies_ip():
    '''获取代理ip'''
    url = "http://www.66ip.cn/mo.php?sxb=&tqsl=10&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea="
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.66ip.cn",
        "Referer": "http://www.66ip.cn/pt.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    }

    resp = requests.get(url=url, headers=headers)
    pat = '	(.*?)<br />'
    result = re.findall(pat, resp.text)
    ip_list = []
    if len(result) > 0:
        for i in result:
            ip_list.append(i.strip().replace('\t', ''))
        # 随机选取一个ip
        ip = random.choice(ip_list)
        return ip
    else:
        print("获取代理ip失败")

if __name__ == '__main__':
    print(proxies_ip())
