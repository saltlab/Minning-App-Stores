 #!/usr/bin/env python
''' Apple AppStore reviews scrapper
    version 2011-04-12
    Tomek "Grych" Gryszkiewicz, grych@tg.pl
    http://www.tg.pl
    
    based on "Scraping AppStore Reviews" blog by Erica Sadun
     - http://blogs.oreilly.com/iphone/2008/08/scraping-appstore-reviews.html
    AppStore codes are based on "appstore_reviews" by Jeremy Wohl
     - https://github.com/jeremywohl/iphone-scripts/blob/master/appstore_reviews
'''

import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient

appStores = {

'United States':      143441
}
#IOS DB info
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_android_1=db_ios.androidAppsCluster

#android DB info
#client_android = MongoClient('localhost', 27017)
#db_android=client_android.Apps 
#collection_android_2=db_android.androidAppsClusterTest

def _print_rawmode(reviews):
    for review in reviews:
         print json.dumps(review)
        
def _getCollection():
     apps=[]
     count=0
     for post in collection_android_1.find().batch_size(30):
         count=count+1
         #print count
         title=(post['title'])
         devName=(post['developer_name'])
         category=(post['category'])
         temp= str(count)+":"+title
         print temp
         clusterID=title+devName
         _setIntialClusterID(title,devName,clusterID)
         title=re.escape(post['title'])
         devName=re.escape(post['developer_name'])

         title_regx = re.compile("^"+title+"[\w|\W]", re.IGNORECASE)
         dev_regx=re.compile("^"+devName+"$",re.IGNORECASE)
        # clusterID=title+devName
         collection_android_1.update(
            {'title':title_regx, 'developer_name':dev_regx, 'category':category}, 
            {'$set': {'android_clusterID':clusterID }},
            multi=True,
            upsert=False )
         
           

         
        
def _setIntialClusterID(title,devName,clusterID):
         collection_android_1.update(
            {'title':title, 'developer_name':devName, 'android_clusterID':{'$exists':False}}, 
            {'$set': {'android_clusterID':clusterID }},
            multi=True,
            upsert=False )
def _find():

    title_regx = re.compile("^iFunny", re.IGNORECASE)
    dev_regx=re.compile("^Facebook"+"$",re.IGNORECASE)
    for post in collection_android_2.find({'title':'iFunny :)'}):
        print post           

if __name__ == '__main__':
    #_find()
   _getCollection()


