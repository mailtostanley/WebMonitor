#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logEntryParser import LogEntryParser
import json
import time

def parseLogFile(filePath):
    try:
        logFile = open(filePath, 'r')
        analyzeResult = {}
        time = ""
        count = 0
        for logEntry in logFile:
            parser = LogEntryParser(logEntry)
            t = parser.getTimeMin()
            if time != t:
                count = 1
                analyzeResult[t] = count
                time = t
            else:
                count += 1
                analyzeResult[t] = count
        return analyzeResult
    except Exception, e:
        print "Exception in parseLogFile: %s" % e
    finally:
        logFile.close()

def parseLogList(logList):
    if logList is None:
        raise Exception("Log list is none")
    analyzeResult = {}
    time = ""
    count = 0
    for logEntry in logList:
        parser = LogEntryParser(logEntry)
        t = parser.getTimeMin()
        if time != t:
            count = 1
            analyzeResult[t] = count
            time = t
        else:
            count += 1
            analyzeResult[t] = count
    return analyzeResult


def transformTimeStamp(di):
    '''
    convert the format string time to timeStamp
    e.g. {"02/Nov/2015:09:59": 1, "03/Nov/2015:19:19": 1}
    to {"1446429540.0": 1, "1446429540.0": 1}
    '''
    transformDict = {}
    for key in di:
        timeStamp = time.mktime(time.strptime(key, '%d/%b/%Y:%H:%M'))
        transformDict[timeStamp] = di[key]
    return transformDict


def getCompleteList(di):
    '''
    in specific time slot, get every minite filled with data
    '''
    completeList = []
    sortedDi = sortDictByKey(di)
    beginTime = int(float(sortedDi[0][0]))
    endTime = int(float(sortedDi[-1][0])) + 60
    for time in range(beginTime, endTime, 60):
        key = float(time)
        if key in di:
            completeList.append({key: di[key]})
        else:
            completeList.append({key: 0})
    return completeList

def splitListByHour(dataList):
    '''
    split the complete list by hour, and group each hour data
    into a single list, then add all of those lists into one list.
    '''
    splitList = []
    hourList = []
    hour_pre = ''
    for dataDict in dataList:
        for key in dataDict:
            hour = time.strftime("%H", time.localtime(key))
        if len(hourList) == 0 or hour == hour_pre:
            hourList.append(dataDict)
        else:
            splitList.append(hourList)
            hourList = []
            hourList.append(dataDict)
        hour_pre = hour
    return splitList

def getRecentDayList(dataList):
    return dataList[-24:]

def apiFilterFile(filePath, api):
    try:
        logFile = open(filePath, 'r')
        filterFile = open(filePath+'.ft', 'w')
        for logEntry in logFile:
            parser = LogEntryParser(logEntry)
            if parser.getPath() == api:
                filterFile.write(logEntry)
    except Exception, e:
        print "Exception in apiFilter: %s" % e
    finally:
        logFile.close()
        filterFile.close()


def apiFilter(filePath, api):
    try:
        logFile = open(filePath, 'r')
        filterList = []
        for logEntry in logFile:
            parser = LogEntryParser(logEntry)
            if parser.getPath() == api:
                filterList.append(logEntry)
        return filterList
    except Exception, e:
        print "Exception in apiFilter: %s" % e
    finally:
        logFile.close()


def sortDictByValue(di):
    return sorted(di.items(), key=lambda x: x[1])


def sortDictByKey(di):
    return sorted(di.items(), key=lambda x: x[0])


def generateJsonFile(data):
    jsonData = json.dumps(data)
    print jsonData
    try:
        jsonFile = open('./log.json', 'w')
        jsonFile.write(jsonData)
    except Exception, e:
        print "Exception in generateJsonFile: %s" % e
    finally:
        jsonFile.close()

def generateJsFile(data):
    try:
        jsFile = open('./logResults.js', 'w')
        jsFile.write('var results = ')
        jsFile.write(json.dumps(data))
    except Exception, e:
        print "Exception in generateJsFile: %s" % e
    finally:
        jsFile.close()


def main():
    filePath = "/Users/eliu/Downloads/box.log"
    api = '/app/box/img/shake.png'
    result = parseLogFile(filePath)
    # result = parseLogList(apiFilter(filePath, api))
    # result = parseLogFile(filePath+'.ft')
    # generateJsFile(sortDictByKey(result))
    # generateJsonFile(sortDictByKey(result))
    # generateJsonFile(result)
    transDict = transformTimeStamp(result)
    # print transDict
    comList = getCompleteList(transDict)
    splitList = splitListByHour(comList)
    # print splitList
    generateJsFile(getRecentDayList(splitList))

if __name__ == '__main__':
    main()

