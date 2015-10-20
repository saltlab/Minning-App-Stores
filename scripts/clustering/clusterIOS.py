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
import urllib2
from elementtree import ElementTree
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
collection_android_1=db_ios.iosApps

#android DB info
client_android = MongoClient('localhost', 27017)
db_android=client_android.Apps 
collection_android_2=db_android.iosApps

def _print_rawmode(reviews):
    for review in reviews:
         print json.dumps(review)
        
def _getCollection():
     apps=[]
     count=0
     for post in collection_android_1.find().batch_size(30):
         count=count+1
         #print count
         name=(post['name'])
         devName=(post['developerName'])
         category=(post['category'])
         temp= str(count)+":"+name
         print temp
         clusterID=name+devName
         _setIntialClusterID(name,devName,clusterID)
         name=re.escape(post['name'])
         devName=re.escape(post['developerName'])

         name_regx = re.compile("^"+name+"[\w|\W]", re.IGNORECASE)
         dev_regx=re.compile("^"+devName+"$",re.IGNORECASE)
         collection_android_1.update(
            {'name':name_regx, 'developerName':dev_regx,'category':category }, 
            {'$set': {'ios_clusterID':clusterID }},
            multi=True,
            upsert=False )
         
           

         
        
def _setIntialClusterID(name,devName,clusterID):
         collection_android_1.update(
            {'name':name, 'developerName':devName, 'ios_clusterID':{'$exists':False}}, 
            {'$set': {'ios_clusterID':clusterID }},
            multi=True,
            upsert=False )
def _find():

    name_regx = re.compile("^iFunny", re.IGNORECASE)
    dev_regx=re.compile("^Facebook"+"$",re.IGNORECASE)
    for post in collection_android_1.find({'name':'iFunny :)'}):
        print post           

if __name__ == '__main__':
    #_find()
   _getCollection()


