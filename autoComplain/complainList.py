# coding: UTF-8 
import socket
import urllib2
import traceback
import MySQLdb
from bs4 import BeautifulSoup
from complainDetail import *

timeout = 10
socket.setdefaulttimeout(timeout)

def getPageNum():
    pageNum = 0
    try:
        f = urllib2.urlopen("http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml")
        content = f.read() 
        soup = BeautifulSoup(content)
        divList = soup.find_all(attrs={'class':'p_page'})[0]
        aList = divList.find_all('a')
        lastPage = aList[-1]['href']
        pageNum = lastPage.split('.')[0].split('-')[-1]
    except IOError:
        print uri, " access error!"
        return -1
    finally:
        f.close()
    return int(pageNum)


def insertDb(table, vlist):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306, db="autocomplain")
    cur=conn.cursor()
    num=int(vlist[0])
    brand=vlist[1]	
    family=vlist[2]
    version=vlist[3]
    abstract=vlist[4]
    detailUrl=vlist[5]
    failure=vlist[6]
    published=vlist[7]
    status=vlist[8]	
    sql = "insert into " + table + "(num,brand,family,version,abstract,detailUrl,failure,published,status,collectTime) values " + "('%s','%s','%s','%s','%s','%s','%s','%s','%s', now())"%(num,brand,family,version,abstract,detailUrl,failure,published,status)  
    #print sql    
    cur.execute("set names gbk")   
    cur.execute(sql.encode("gbk"))   
    conn.commit()
	 
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
					typeStr[failureType[ord(alpha)-baseIndex]['name'].decode("gbk")] = j['title'].decode("gbk")
					break			
	return typeStr

def fetchFailureTye(uri):
	try:
	    f = urllib2.urlopen(uri)
	    content = f.read() 
	    rawType = content.split("=")[1]
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
        for i in range(1,len(trList)):
            typeDict = {}
            vlist = []
            tdList = trList[i].find_all('td')            
            vlist.append(tdList[0].string)            
            vlist.append(tdList[1].string)            
            vlist.append(tdList[2].string)            
            vlist.append(tdList[3].string)            
            vlist.append(tdList[4].string)
            vlist.append("http://www.12365auto.com%s"%tdList[4].a['href'])            
            fetchDetail(int(tdList[0].string),"http://www.12365auto.com%s"%tdList[4].a['href'])           
            flist = []
            if tdList[5].string != None:
                typeDict = getFailureTye(tdList[5].string, failureType)			
            for i in typeDict.items():				
                flist.append(':'.join(i))            
            if tdList[2]['fw'] != '':				
                flist.append(tdList[2]['fw'])            
            vlist.append(','.join(flist))            
            vlist.append(tdList[6].string)            
            vlist.append(tdList[7].em.string)            
            insertDb("complainList", vlist)
    except Exception,e:
        print uri, " access error!"        
    finally:
        f.close()

if __name__ == "__main__":
    failureTypeUri = "http://www.12365auto.com/js/cTypeInfo.js"
    failureType = fetchFailureTye(failureTypeUri)
    if failureType == -1: exit(-1)	
    pageNum = getPageNum()
    if pageNum == -1: exit(-2)
    print "total page:", pageNum
    #pageNum = 2
    for pageNum in range(1,pageNum):
        print "page:", pageNum
        complainListUri = "http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-%s.shtml"%pageNum
        fetchComplainList(complainListUri)
