#This code also looks for app-pairs but this time relaxes the requirements on the app and Dev name to also find close matches of the app.
import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
from pymongo import ReturnDocument

#IOS DB info
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_ios=db_ios.iOSApps

#android DB info
client_android = MongoClient('localhost', 27017)
db_android=client_android.Apps 
collection_android=db_android.AndroidApps

def _print_rawmode(reviews):
    for review in reviews:
         print json.dumps(review)
        
def _getCollection():
     apps=[]
     count=0
     matches=0
     for post in collection_android.find({'processed':{'$exists':False}},no_cursor_timeout=True):
         count=count+1
         android_app_id=post['app_id']
         collection_android.find_one_and_update({"app_id":android_app_id},{'$set':{'processed':True}})
        
         android_title=re.escape(post['title'])
         android_developer_name=re.escape(post['developer_name'])

         title_regx = re.compile("^"+android_title, re.IGNORECASE)
         dev_regx=re.compile("^"+android_developer_name,re.IGNORECASE)

         updated=collection_ios.find_one({"name":title_regx, "developerName":dev_regx})
         if updated is not None:
            collection_android.find_one_and_update({"app_id":android_app_id},{'$set':{'hasAppPair':True}})
            print "Android AppName:"+post['title']
            print "iOS AppName:"+ updated['name']
            matches=matches+1
            print "matches:" +str(matches)
            print "Apps processed:" +str(count)
            print "*******"


if __name__ == '__main__':

   apps=_getCollection()


