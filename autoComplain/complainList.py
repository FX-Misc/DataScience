# coding: UTF-8 
import socket
import urllib2
import traceback
import MySQLdb
import time
from bs4 import BeautifulSoup
from complainDetail import *

timeout = 10
socket.setdefaulttimeout(timeout)
MaxBuffer = 20 # sync page update
buffer = 0
def getPageNum():
    pageNum = 0
    tryNum = 3
    tn = 0
    while tn < tryNum:
        try:
            f = urllib2.urlopen("http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml")
            content = f.read() 
            soup = BeautifulSoup(content)
            divList = soup.find_all(attrs={'class':'p_page'})[0]
            aList = divList.find_all('a')
            lastPage = aList[-1]['href']
            pageNum = lastPage.split('.')[0].split('-')[-1]
            break
        except Exception,e:
            print e
            tn = tn + 1
            print uri, " access error!"
            print "try ", tn, "time"
            time.sleep(5)    
    if tn==tryNum:
        print "get Page Num Error!"
        return -1
    return int(pageNum)

def getMaxNumOfComplain():
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306, db="autocomplain")
    cur=conn.cursor()
    sql = "select max(num) from complainList"    
    cur.execute(sql)
    conn.commit();
    num = cur.fetchone()
    #print 1
    if num[0]:        
        return int(num[0])
    else:
        return 0
 
def exitsInDb(num):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306, db="autocomplain")
    cur=conn.cursor()
    sql = "select num from complainList where num=%s"%num    
    cur.execute(sql)
    conn.commit();
    num = cur.fetchone()
    #print num        
    if num: 
        print "exits"    
        return 1 # exits
    else: 
        #print "not exits"
        return 0 # not exits

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
	except Exception,e:
		print uri, " access error!"
		return -1	
	return failureType


def fetchComplainList(uri):
    tryNum = 3
    tn = 0
    while tn < tryNum:
        try:
            f = urllib2.urlopen(uri)
            content = f.read()
            soup = BeautifulSoup(content)
            trList =  soup.table.find_all('tr')        
            for i in range(1,len(trList)):
                typeDict = {}
                vlist = []
                tdList = trList[i].find_all('td')
                num  = tdList[0].string                
                if exitsInDb(num) == 0:
                    print "continue"
                    #continue                
                    vlist.append(num) # num            
                    vlist.append(tdList[1].string) # brand         
                    vlist.append(tdList[2].string) # family         
                    vlist.append(tdList[3].string) # version          
                    vlist.append(tdList[4].string) # abstract
                    vlist.append("http://www.12365auto.com%s"%tdList[4].a['href'])  #  detailUrl          
                    fetchDetail(int(tdList[0].string),"http://www.12365auto.com%s"%tdList[4].a['href'])           
                    flist = []
                    if tdList[5].string != None:
                        typeDict = getFailureTye(tdList[5].string, failureType)			
                    for i in typeDict.items():				
                        flist.append(':'.join(i))            
                    if tdList[2]['fw'] != '':				
                        flist.append(tdList[2]['fw'])            
                    vlist.append(','.join(flist))  #          
                    vlist.append(tdList[6].string) # published          
                    vlist.append(tdList[7].em.string)  # status           
                    insertDb("complainList", vlist)
                else:
                    continue
            break
        except Exception,e:
            print e
            tn  = tn  + 1
            print uri, " access error!"
            print "try ", tn, "time"
            time.sleep(5)            
    if tn==tryNum:
        print "Cannot fetch page!"
        return -1
    return 0

if __name__ == "__main__":
    failureTypeUri = "http://www.12365auto.com/js/cTypeInfo.js"
    failureType = fetchFailureTye(failureTypeUri)
    if failureType == -1: exit(-1)	
    pageNum = getPageNum()
    if pageNum == -1: exit(-2)
    print "total page:", pageNum
    #pageNum = 2
    for p in range(1501,pageNum):
        print "page:", p
        complainListUri = "http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-%s.shtml"%p
        fetchComplainList(complainListUri)    
    print "Auto Complain Collection Updated"
