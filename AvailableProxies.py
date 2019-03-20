#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: Pu MingZheng
@license: Apache Licence 
@file: AvailableProxies.py
@time: 2019/3/20 9:11
"""

import requests
import time
import csv

from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class AvailableProxies(object):
    def __init__(self):
        self.url = 'http://www.xicidaili.com/'
        self.ua = UserAgent()
        self.headers = {'User-Agent': self.ua.random}

    def parse(self):
        request = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(request.text, 'lxml')
        return soup

    def get_ip_list(self, soup):
        ip_text = soup.find_all('tr', {'class': 'odd'})  # 获取带有IP地址的表格的所有行
        ip_list = []
        for i in range(len(ip_text)):
            ip_tag = ip_text[i].findAll('td')
            ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()  # 提取出IP地址和端口号
            ip_list.append(ip_port)
        print("共收集到了{}个代理IP".format(len(ip_list)))
        # print(ip_list)
        return ip_list

    def val_ip(self, proxies: 'List[dict]'):
        unavailable = 0
        available = 0
        available_proxies = []
        for proxy in proxies:
            try:
                proxy_host = proxy
                protocol = 'https' if 'https' in proxy_host else 'http'
                proxies = {protocol: proxy_host}
                response = requests.get('https://www.baidu.com', proxies=proxies, timeout=2)
                if response.status_code != 200:
                    unavailable += 1
                    # print(proxy_host, 'bad proxy')
                else:
                    available += 1
                    # available_proxies.append(proxies)
                    available_proxies.append(proxy_host)
                    print(proxy_host, 'success proxy')
            except Exception as e:
                print(e)
                unavailable += 1
                continue
        print('success proxy num : ', available)
        print('bad proxy num : ', unavailable)
        return available_proxies


if __name__ == '__main__':
    proxies = AvailableProxies()
    parse = proxies.parse()
    ip_list = proxies.get_ip_list(parse)
    available_proxies = proxies.val_ip(ip_list)
    print(available_proxies)

    filename = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) + '.csv'
    with open(filename, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        for i in available_proxies:
            csv_writer.writerow([i])
