#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests
import time


def get_index(index_url):

    response = requests.get(url=index_url)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(response.json())


def parse_index(html):
    proxy_list = []
    for i in range(len(html['data'])):
        ip = html['data'][i]['ip']
        port = html['data'][i]['port']
        e_time = html['data'][i]['expire_time']
        # print(ip,port)
        # print(e_time)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        m_str = re.split(':|\s', e_time)
        now_str = re.split(':|\s', now_time)
        # print(m_str)
        # print(now_str)
        if int(int(m_str[1])+24) > int(int(now_str[1])+24):

            if int(int(m_str[2])+120) - int(int(now_str[2])+60) > 20:
                # print(e_time)
                proxy_ip = 'https://{0}:{1}'.format(ip, port)
                # print(proxy_ip)
                # if len(proxy_list) < 2:
                if len(proxy_list) < 6:
                    proxy_list.append(proxy_ip)
        else:
            if int(int(m_str[2])+60) - int(int(now_str[2])+60) > 20:
                # print(e_time)
                proxy_ip = 'https://{0}:{1}'.format(ip, port)
                # print(proxy_ip)
                # if len(proxy_list) < 2:
                if len(proxy_list) < 6:
                    proxy_list.append(proxy_ip)

    print(len(proxy_list))
    return proxy_list


def save_file(proxy_list):
    with open('/home/you/codes1/amazonstores/amazonstores/proxies.txt','w') as f:
        for proxy in proxy_list:
            print(proxy)
            f.write(proxy+'\n')
        # f.write('=============')
        print('=========')


def main():
    url = 'http://webapi.http.zhimacangku.com/getip?num=13&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=1&lb=1&sb=0&pb=5&mr=1&regions='
    html = get_index(url)
    if html:
        proxy_list = parse_index(html)
        # if len(proxy_list) > 1:
        if len(proxy_list) > 4:
            save_file(proxy_list)
        else:
            time.sleep(4)
            main()


if __name__ == '__main__':
    while True:
        main()
        time.sleep(1200)
