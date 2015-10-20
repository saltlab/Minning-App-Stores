#This script assumes you have 2 datasets one with android apps and the other with iOS apps and you are trying to find app-pairs.
#It uses the appName and DevName to search for app-pairs and merges the results into one single collection.

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
collection_ios=db_ios.iosApps

#android DB info
client_android = MongoClient('localhost', 27017)
db_android=client_android.Apps 
collection_android=db_android.androidApps

def _print_rawmode(reviews):
    for review in reviews:
         print json.dumps(review)
        
def _getCollection():
     apps=[]
     count=0
     matches=0
     for post in collection_android.find().batch_size(30):
         count=count+1
         android_app_id=post['android_app_id']
         android_title=post['android_title']
         android_developer_name=post['android_developer_name']
         android_category=post['android_category']
         android_free=post['android_free']
         android_version_code=post['android_version_code']
         android_version_string=post['android_version_string']
         android_installation_size=post['android_installation_size']
         android_downloads=post['android_downloads']
         android_star_rating=post['android_star_rating']
         android_snapshot_date=post['android_snapshot_date']
         android_metadata_url=post['android_metadata_url']
         
         android_title=re.escape(post['android_title'])
         android_developer_name=re.escape(post['android_developer_name'])

         title_regx = re.compile("^"+android_title+"$", re.IGNORECASE)
         dev_regx=re.compile("^"+android_developer_name+"$",re.IGNORECASE)


         #print android_title
         temp= str(count)+":"+android_title
         print temp
         updated=collection_ios.find_one_and_update({"ios_name":title_regx, "ios_developerName":dev_regx}, {'$set': {   'android_app_id':android_app_id, 
                                                                                    'android_title':android_title,
                                                                                     'android_developer_name':android_developer_name, 
                                                                                     'android_category':android_category, 
                                                                                     'android_free':android_free, 
                                                                                     'android_version_code':android_version_code, 
                                                                                     'android_version_string':android_version_string, 
                                                                                     'android_installation_size':android_installation_size, 
                                                                                     'android_downloads':android_downloads,
                                                                                     'android_star_rating':android_star_rating,
                                                                                     'android_snapshot_date':android_snapshot_date,
                                                                                     'android_metadata_url':android_metadata_url    }  } , return_document=ReturnDocument.AFTER)
         if updated is not None:
            matches=matches+1
            print "matches:" +str(matches)
          
    


if __name__ == '__main__':

   apps=_getCollection()


