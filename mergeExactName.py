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
collection_ios=db_ios.iosAppsPilot

#android DB info
client_android = MongoClient('localhost', 27017)
db_android=client_android.Apps 
collection_android=db_android.androidAppsPilot

def _print_rawmode(reviews):
    for review in reviews:
         print json.dumps(review)
        
def _getCollection():
     apps=[]
     for post in collection_android.find():
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
         android_url=post['android_url']



         print android_title
         collection_ios.find_one_and_update({"ios_name":android_title}, {'$set': {   'android_app_id':android_app_id, 
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
                                                                                     'android_metadata_url':android_metadata_url, 
                                                                                     'android_url':android_url,         }  })
         
     
     return apps
     #return collection.find_one()
def _add_reviews(url,reviews):
     data_string = json.dumps(reviews)
     print collection.find_one_and_update({"url":url}, {'$set': {'reviews':json.loads(data_string)}  })

def _add_reviews_test(url,reviews):
    for review in reviews:
         print type(review)  

if __name__ == '__main__':

   apps=_getCollection()


