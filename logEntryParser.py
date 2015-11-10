#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

class LogEntryParser():
    def __init__(self, logEntry):
        self.logEntry = logEntry

    def getTime(self):
        time_re = re.compile(r'\[(.*?)\]')
        time = re.findall(time_re, self.logEntry)[0]
        return time.split(' ')[0]

    def getTimeMin(self):
        time_re = re.compile(r'\[(.*?)\]')
        time = re.findall(time_re, self.logEntry)[0]
        return time.split(' ')[0][:-3]

    def getPath(self):
        path_re = re.compile(r'GET (.*?) HTTP/1.1')
        result = re.findall(path_re, self.logEntry)
        if len(result) != 0:
            return result[0]
        else:
            return ''

    def getUserAgent(self):
        pass

if __name__ == '__main__':
    logEntry = '123.151.42.50 - - [01/Nov/2015:06:57:43 +0800]\
     "GET /app/box/js/style.min.js HTTP/1.1" 200 542 \
    "http://qing.sensoro.com/app/box/mobile/562e0a2f8cc4add66cc20582?\
    appid=wxd4524fc37371a13d&wechat=true&nonceStr=dd3cb24e" \
    "Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; GT-I9082C Build/JDQ39) \
    AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025478 Mobile \
    Safari/533.1 MicroMessenger/6.2.5.53_r2565f18.621 NetType/WIFI Language/zh_CN" \
    "1.26.197.247" - - - -'
    parser = LogEntryParser(logEntry)
    print parser.getPath()