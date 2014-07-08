#/usr/bin/python

import urllib2
import pymongo as pm
import traceback

stockfile = open('code.bak','r')
client = pm.MongoClient("localhost",27017)
db = client.stockdb
stocks = db.stockName
stockRecord = db.stockRecord
termList = ['today_open_price', 'yesterday_close_price', 'current_price', 'today_highest', 'today_lowest', 'bid_buy', 'bid_sail', 'total_deal', 'total_money', 'buy_1_count', 'buy_1_price', 'buy_2_count', 'buy_2_price', 'buy_3_count', 'buy_3_price', 'buy_4_count', 'buy_4_price', 'buy_5_count', 'buy_5_price', 'sail_1_count', 'sail_1_price', 'sail_2_count', 'sail_2_price', 'sail_3_count', 'sail_3_price', 'sail_4_count', 'sail_4_price', 'sail_5_count', 'sail_5_price', 'date', 'time', 'last']

for stock in stockfile:
    uri =  "http://hq.sinajs.cn/list=%s"%stock
    try:
        f = urllib2.urlopen(uri)
        content =  f.readline().split('=')[1]
        content = content[0:-2]
        record = dict()
        if len(content) > 2:
            #print "stock:",content.decode('gbk').strip('"')
            clist = content.decode('gbk').strip('"').split(",")
            #print len(clist)
            sn = { "_id":stock.strip('\n'), "name":clist[0] }
            #print sn
            for i in range(0,len(termList)):
                record[termList[i]] = clist[i+1]
            #print record
            record['code_id'] = stock.strip('\n')
            date = record['date']
            record['date'] = int(''.join(date.split("-")))
            record['datestr'] = date
            stockRecord.insert(record)
            #stocks.insert(sn)
        else:
            print "stock:","null" 
    except:
        print stock,"error"
        continue
