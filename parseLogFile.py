#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logEntryParser import LogEntryParser
import json

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
        jsFile = open('./logResult.js', 'w')
        jsFile.write('var result = ')
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
    generateJsFile(sortDictByKey(result))
    # generateJsonFile(sortDictByKey(result))
    # generateJsonFile(result)


if __name__ == '__main__':
    main()

