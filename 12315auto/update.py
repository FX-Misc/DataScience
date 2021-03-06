# coding: UTF-8 
import urllib2
import traceback
import MySQLdb
from bs4 import BeautifulSoup

from complainDetail import *
from complainList import *

def updateComplainList(uri):
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
                    return -2
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
    for p in range(1,pageNum):
        print "page:", p
        complainListUri = "http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-%s.shtml"%p
        if updateComplainList(complainListUri) == -2:
            print "Updated!"
            break
    print "Auto Complain Collection Updated"
            
    