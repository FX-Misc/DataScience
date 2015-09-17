# coding: UTF-8 
import socket
import urllib2
import traceback
#import MySQLdb
import time
from bs4 import BeautifulSoup
import index
import pageNum

timeout = 20
socket.setdefaulttimeout(timeout)




def fetchVerbAtPage(url):
    tryNum = 3
    tn = 0
    while tn < tryNum:
        try:
            f = urllib2.urlopen(url)
            content = f.read()
            soup = BeautifulSoup(content)
            leftVerbTable = soup.find(attrs={'class':'CtgryUlL'})  
            rightVerbTable = soup.find(attrs={'class':'CtgryUlR'}) 
            
            leftVerbLiList = leftVerbTable.find_all('li')
            rightVerbLiList = rightVerbTable.find_all('li')
            
            for i in leftVerbLiList:
                a = i.find('a')
                print a['href']+"?dictCode=NHGKT", a.string
            
            for i in rightVerbLiList:
                a = i.find('a')
                print a['href']+"?dictCode=NHGKT", a.string     
            break
        except Exception,e:
            print e
            tn  = tn  + 1
            #print url, " access error!"
            #print "try ", tn, "time"
            time.sleep(5)            
    if tn==tryNum:
        #print "Cannot fetch page!"
        return -1
    return 0

if __name__ == "__main__":
    url = index.kanaAlpha[0]
    num = pageNum.pn[url]
    #print url
    #print num
    for i in range(1, num+1):
        _url = url+'/'+str(i)
        #print _url
        if(fetchVerbAtPage(_url)==-1):
            print _url, "ERROR."
          
    print "Finished"
