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
collection_ios=db_ios.matches

#android DB info
client_android = MongoClient('localhost', 27017)
db_android=client_android.Apps 
collection_android=db_android.androidAppsPilot

def _print_rawmode(reviews):
    for review in reviews:
         print json.dumps(review)
        
def _getCollection():
     apps=[]
     for post in collection_ios.find():
         ios_rating=post['ios_rating']
         ios_starsRatingCurrentVersion=ios_rating['starsRatingCurrentVersion']
         ios_starsVersionAllVersions=ios_rating['starsVersionAllVersions']
         ios_ratingsCurrentVersion=ios_rating['ratingsCurrentVersion']
         ios_ratingsAllVersions=ios_rating['ratingsAllVersions']
         _add_fields(post['ios_url'],ios_starsRatingCurrentVersion,ios_starsVersionAllVersions,ios_ratingsCurrentVersion,ios_ratingsAllVersions)

def _add_fields(url,ios_starsRatingCurrentVersion,ios_starsVersionAllVersions,ios_ratingsCurrentVersion,ios_ratingsAllVersions):
     print collection_ios.find_one_and_update({"ios_url":url}, {'$set': {'ios_starsRatingCurrentVersion':ios_starsRatingCurrentVersion,
                                                                         'ios_starsVersionAllVersions':ios_starsVersionAllVersions,
                                                                         'ios_ratingsCurrentVersion':ios_ratingsCurrentVersion,
                                                                         'ios_ratingsAllVersions':ios_ratingsAllVersions}  })

 

if __name__ == '__main__':

   _getCollection()


