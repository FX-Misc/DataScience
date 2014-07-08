#!/usr/bin/python
import sys
import pymongo as pm
from datetime import date  
def main(argv):
    client = pm.MongoClient()
    db = client.stockdb
    stockName = db.stockName
    stockRecord = db.stockRecord
    partten = {'code_id':argv[0],'datestr':argv[1]}
    result = stockRecord.find_one(partten)
    invest = float(argv[2])*1.0 
    print 'invest:',invest
    print 'date:',argv[1]
    print 'hightest:', float(result['today_highest'])
    count = invest / float(result['today_highest'])
    today = date.today().__str__() 
    partten_c = {'code_id':argv[0],'datestr':today}
    result_c = stockRecord.find_one(partten_c)
    today_lowest = result_c['today_lowest']
    profit = count * float(today_lowest) - invest
    print '-'*20
    print 'profit:',profit
    print 'date:', today
    print 'lowest:',today_lowest 
    
    
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Param Error!\nUsage:\n  python predict.py code date[2014-01-01] money"
        sys.exit(-1)
    main(sys.argv[1:])     
