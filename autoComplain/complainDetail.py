# coding: UTF-8 
import urllib2
import traceback
import MySQLdb
from bs4 import BeautifulSoup
import time
import os

def insertData(table, cols, vlist):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306, db="autocomplain")
    cur=conn.cursor()   	
    sql = "insert into " + table + cols + "values " + vlist         
    cur.execute("set names gbk") 
    try:    
        cur.execute(sql.encode('gbk'))
        #cur.execute(sql)
        conn.commit()
    except Exception,e:
        print "insert error!", e
        return -1

def saveImage(cnum, uri):
    tryNum = 3
    tn = 0
    path = os.path.dirname(os.path.abspath(__file__))
    while tn < tryNum:
        try:
            img = urllib2.urlopen(uri)
            content = img.read()
            imageFileName = path+'/img/'+str(cnum)+'.jpg'
            print imageFileName
            f = open(imageFileName, 'wb')
            f.write(content)
            return imageFileName        
        except Exception,e:
            tn = tn + 1
            print e
            print uri, " access error!"
            print "try ", tn, "time"
            time.sleep(5)
    if tn==tryNum:
        print "get Page Num Error!"
        return "cannot fetch image"
		

def fetchDetail(cnum, uri):
    tryNum = 3
    tn = 0
    print "Detail Page:",uri
    while tn < tryNum:
        try:
            f = urllib2.urlopen(uri)
            content = f.read() 
            soup = BeautifulSoup(content)       
            divList = soup.find_all(attrs={'class':'jbqk'})[0]
            liList =  divList.find_all('li')
            published = liList[-1].contents[1].strip()
            divList = soup.find_all(attrs={'class':'tsnr'})[0]
            pList = divList.find_all('p')
            imgList = []
            c = ""
            for i in pList:
                if i.find('img') != None:
                    imgUri = i.find('img')['src']
                    imgSavePath = saveImage(cnum, "http://www.12365auto.com/%s"%imgUri)
                    imgList.append(imgSavePath)
                else:
                    c = i.string
                    #c = i.contents
                    #print "c:",
                    #print repr(c)                   
            img = ','.join(imgList)                  
            divList = soup.find_all(attrs={'class':'tshf'})[0]
            reply = divList.p.string       
            cols = "(cnum, published, img, content, reply, collectTime)"
            vlist = "("+"'%s','%s','%s','%s','%s'"%(cnum, published, img, c, reply)+",now()"+")"
            insertData("complaindetail", cols, vlist)
            print "complain:",cnum
            break            
        except Exception,e:
            tn = tn + 1            
            print uri, " access error!"
            print e
            print "try ", tn, "time"
            time.sleep(5)
    if tn==tryNum:
        print "get Page Num Error!"
        return -1    