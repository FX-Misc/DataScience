# coding: UTF-8 
#/usr/bin/python
import urllib2
import traceback
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

def getFailureTye(str, failureType):
	indexList = str.split(",")	
	typeStr = {}
	baseIndex = ord('A')
	for i in indexList:
		if i != '':
			alpha = i[0]
			num = i[1:]			
			for j in failureType[ord(alpha)-baseIndex]['items']:
				if j['id'] == int(num):
					typeStr[failureType[ord(alpha)-baseIndex]['name']] = j['title']
					break			
	return typeStr

def fetchFailureTye(uri):
	try:
	    f = urllib2.urlopen(uri)
	    content = f.read().decode('gbk') 
	    rawType = content.encode('UTF-8').split("=")[1]
	    failureType = eval(rawType)    
	except IOError:
		print uri, " access error!"
		return -1
	finally:
		f.close()
	return failureType


def fetchComplainList(uri):
	try:
		f = urllib2.urlopen(uri)
		content = f.read()	
		soup = BeautifulSoup(content)
		trList =  soup.table.find_all('tr')
		typeDict = {}
		for i in range(1,10):
			tdList = trList[i].find_all('td')
			print tdList[0].string
			print tdList[1].string.encode("UTF-8")
			print tdList[2].string.encode("UTF-8")
			print tdList[3].string.encode("UTF-8")
			print tdList[4].string.encode("UTF-8"), "http://www.12365auto.com%s"%tdList[4].a['href']
			if tdList[5].string != None:
				typeDict = getFailureTye(tdList[5].string, failureType)			
			for i in typeDict.items():
				print ':'.join(i),
			print tdList[2]['fw'].encode("UTF-8")
			print tdList[6].string.encode("UTF-8")
			print tdList[7].em.string.encode("UTF-8")  
			print "-"*20 
	except IOError:
		print uri, " access error!"
		exit(-1)
	finally:
		f.close()

if __name__ == "__main__":
	failureTypeUri = "http://www.12365auto.com/js/cTypeInfo.js"
	failureType = fetchFailureTye(failureTypeUri)
	if failureType==-1: exit(-1)
	pageNum = 1
	complainListUri = "http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-%s.shtml"%pageNum
	fetchComplainList(complainListUri)
