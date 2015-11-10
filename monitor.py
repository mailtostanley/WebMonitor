#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2
import base64
import logging
import os
from sendEmail import sendEmail
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep
httplib2.debuglevel = 1

path = os.getcwd()
logPath = os.path.join(path, "monitor.log")
logger = logging.getLogger("monitorlogger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(logPath)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(filename)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def sendAPI(url):
    # we will totall try 3 times if send api fails
    retryCount = 3
    # set timeout 10s, over 10s, we assume it fails.
    http = httplib2.Http(timeout=10)
    email = "test@sensoro.com"
    password = "123456"
    auth = base64.encodestring(email + ':' + password)
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Cache-Control": "no-cache",
                "Authorization": "Basic " + auth,
                "Connection": "Keep-Alive",
                }
    while True:
        try:
            res, data = http.request(url, "GET", headers=headers)
            if not parseResponse(res):
                raise Exception("Response is not correct.")
            sleep(300)
        except Exception, e:
            if retryCount > 0:
                retryCount -= 1
                logger.warning("Exception: %s" % e)
                logger.warning("Send API retry...")
                sleep(30)
                http = httplib2.Http(timeout=10)
                continue
            logger.error("Send API error.")
            logger.error("Exception: %s" % e)
            msg = "There is server API error. The URL is: %s.\r\n Exception is: %s." % (url, e)
            sendEmail(msg)
            # we need to reset retryCount here
            retryCount = 3
            sleep(3600)
            continue

def getApiList():
    try:
        path = os.getcwd()
        filePath = os.path.join(path, "get_api.txt")
        apiFile = open(filePath, "r")
        apiList = []
        for line in apiFile:
            apiList.append(line.strip())
        return apiList
    except Exception, e:
        logger.error("Can not open get_api.txt file.")
        logger.error("Exception: %s" % e)
    finally:
        apiFile.close()

def parseResponse(response):
    if response['status'] == "200":
        return True
    else:
        return False

def main():
    
    try:
        apiList = getApiList()
        pool = ThreadPool(len(apiList))
        pool.map(sendAPI, apiList)
        pool.close()
        pool.join()
    except Exception, e:
        logger.error("A exception is occourred.")
        logger.error("Exception: %s" % e)

if __name__ == "__main__":
    # apiList = getApiList()
    # for i in apiList:
    #     print i
    url = "http://www.sensoro.xxm/axc"
    sendAPI(url)
    # main()
