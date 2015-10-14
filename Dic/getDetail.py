 # -*- coding:utf-8 -*-
#html_doc = '''<div><a href="http://www.weblio.jp/content/%E5%BD%A2%E5%AE%B9%E5%8B%95%E8%A9%9E" title="形容動詞の意味" class=crosslink>形容動詞</a>「<a href="http://www.weblio.jp/content/%E3%82%A2%E3%83%BC%E3%83%86%E3%82%A3%E3%83%95%E3%82%A3%E3%82%B7%E3%83%A3%E3%83%AB" title="アーティフィシャルの意味" class=crosslink>アーティフィシャル</a>だ」が、<a href="http://www.weblio.jp/content/%E6%8E%A5%E5%B0%BE%E8%AA%9E" title="接尾語の意味" class=crosslink>接尾語</a>「さ」により<a href="http://www.weblio.jp/content/%E4%BD%93%E8%A8%80" title="体言の意味" class=crosslink>体言</a>化した形。<br><br class=nhgktD><div><!--AVOID_CROSSLINK--><p class=nhgktL>終止形</p><p class=nhgktR>アーティフィシャルだ&nbsp;&nbsp;<a href="http://www.weblio.jp/content/%E3%82%A2%E3%83%BC%E3%83%86%E3%82%A3%E3%83%95%E3%82%A3%E3%82%B7%E3%83%A3%E3%83%AB" title="アーティフィシャル">&raquo; 「アーティフィシャル」の意味を調べる</a></p><!--/AVOID_CROSSLINK--><br class=clr></div>'''

#from bs4 import BeautifulSoup
#soup = BeautifulSoup(html_doc, 'html.parser')
#a = [text for text in soup.stripped_strings]
#print ''.join(a[:-1])


import socket
import urllib2
import traceback
import re
#import MySQLdb
import time
from bs4 import BeautifulSoup
#from complainDetail import *

timeout = 10
socket.setdefaulttimeout(timeout)

def fetchDetail(link, word):
    tryNum = 3
    tn = 0
    while tn < tryNum:
        details = []
        try:
            f = urllib2.urlopen(link)
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            main = soup.find(attrs={'class':'Nhgkt'})  
            left = soup.find_all(attrs={'class':'nhgktL'})
            right = soup.find_all(attrs={'class':'nhgktR'})           
            if(left):
                for text in main.stripped_strings: 
                    if(re.match(u'終止形$', text)!=None):break
                    details.append(text)
                print '#'.join(details).encode('utf8'),
                print '%',left[0].string.encode('utf8'), ':',                           
                aList = right[0].find_all('a')
                for a in aList:
                  print a['title'].encode('utf8'),
                print
            else:
                for text in main.stripped_strings:
                    if(u'»' in text):break
                    details.append(text)
                print '#'.join(details).encode('utf8')
                 
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
    
    wordsUrlList = open('verb_ok.txt')
    for line in wordsUrlList.readlines():
        l = line.split(' ')
        link = l[0]
        word = l[1].strip('\n')
        print word, '%', link, '%',
        
        if(fetchDetail(link, word)==-1):
            print link, word, "ERROR."
          
    print "Finished"
    
    
    #indexUrl = "http://www.weblio.jp/category/dictionary/nhgkt/aa"
    #f = urllib2.urlopen(indexUrl)
    #content = f.read()
    #soup = BeautifulSoup(content, 'html.parser')
    #urlTable = soup.find(attrs={'class':'kanaAlpha'})
    #aList = urlTable.find_all('a')
    #for a in aList:
    #    print '"'+a['href']+'",'

