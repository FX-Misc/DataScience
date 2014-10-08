# coding: UTF-8 
import urllib2
import traceback
import MySQLdb
from bs4 import BeautifulSoup
import time
import os

def insertData(table, cols, vlist):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='fnst1234',port=3306, db="autocomplain", charset="utf8")
    cur=conn.cursor()   	
    sql = "insert into " + table + cols + "values " + vlist   
    try:       
        cur.execute(sql)      
        conn.commit()
    except Exception,e:
        print "insert error! utf8", e
        try:
            cur.execute(sql.encode("latin-1").decode('gbk'))        
            conn.commit()
        except Exception,e:
            print "insert error! latin-1", e
            return -1
        return -1

def saveImage(cnum, uri):
    tryNum = 3
    tn = 0
    path = os.path.dirname(os.path.abspath(__file__))
    while tn < tryNum:
        try:
            img = urllib2.urlopen(uri.encode("gbk"))
            content = img.read()
            imageFileName = path+'\\img\\'+str(cnum)+'.jpg'
            #print imageFileName
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
            soup = BeautifulSoup(content.decode('gbk','ignore'))            
            divList = soup.find_all(attrs={'class':'jbqk'})[0]
            liList =  divList.find_all('li')
            published = liList[-1].contents[1].strip()
            divList = soup.find_all(attrs={'class':'tsnr'})[0]            
            pList = divList.find_all('p')            
            cnt = ""
            images = []
            if len(pList) < 2:
                c = pList[0].string               
                #print c
            else:
                c = pList[1].string
                imgList = pList[0].find_all("img")                
                idx = 0
                for i in imgList:
                    imgUri = i["src"]
                    print imgUri
                    pic = "%s_%s"%(cnum,idx)
                    imgSavePath = saveImage(pic, "http://www.12365auto.com/%s"%imgUri)
                    #print "imgpath:", imgSavePath
                    images.append(imgSavePath)
                    idx = idx + 1                    
            img = ','.join(images)
            print img.decode('gbk')
            divList = soup.find_all(attrs={'class':'tshf'})[0]
            reply = divList.p.string       
            cols = "(cnum, published, img, content, reply, collectTime)"
            vlist = "("+"'%s','%s','%s','%s','%s'"%(cnum, published, img.decode('gbk').replace('\\','\\\\'), c, reply)+",now()"+")"
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