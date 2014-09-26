# coding: UTF-8 
import urllib2
import traceback
import MySQLdb
from bs4 import BeautifulSoup

def insertData(table, cols, vlist):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306, db="autocomplain")
    cur=conn.cursor()   	
    sql = "insert into " + table + cols + "values " + vlist  
    #print sql    
    cur.execute("set names gbk") 
    try:    
        cur.execute(sql.encode("gbk"))
        conn.commit()
    except Exception,e:
        return -1


def fetchDetail(cnum, uri):
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
                imgList.append("http://www.12365auto.com/%s"%imgUri)
            else:
                c = i.string        
        img = ','.join(imgList)                  
        divList = soup.find_all(attrs={'class':'tshf'})[0]
        reply = divList.p.string       
        cols = "(cnum, published, img, content, reply, collectTime)"
        vlist = "("+"'%s','%s','%s','%s','%s'"%(cnum, published, img, c, reply)+",now()"+")"
        insertData("complaindetail", cols, vlist)
        print "complain:",cnum        
    except Exception,e:
        print uri, " access error!"
        return -1
    finally:
        f.close()