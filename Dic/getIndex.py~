# coding: UTF-8 
import socket
import urllib2
import traceback
#import MySQLdb
import time
from bs4 import BeautifulSoup
#from complainDetail import *

timeout = 10
socket.setdefaulttimeout(timeout)



if __name__ == "__main__":
    indexUrl = "http://www.weblio.jp/category/dictionary/nhgkt/aa"
    f = urllib2.urlopen(indexUrl)
    content = f.read()
    soup = BeautifulSoup(content)
    urlTable = soup.find(attrs={'class':'kanaAlpha'})
    aList = urlTable.find_all('a')
    for a in aList:
        print '"'+a['href']+'",'
