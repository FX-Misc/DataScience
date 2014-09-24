# coding: UTF-8 
#/usr/bin/python
import urllib2
import traceback
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit


pageNum = 1
uri = "http://www.12365auto.com/js/cTypeInfo.js"
f = urllib2.urlopen(uri)
content = f.read().decode('gbk') 
rawType = content.encode('UTF-8').split("=")[1]
failureType = eval(rawType)

indexDict = {1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"}
print indexDict[1]
print failureType[0]['name']
print failureType[0]['items'][0]['title']