import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
import os
import errno

#IOS DB info
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_ios=db_ios.matches10Android

        
def _getCollection():
     apps=[]
     totalIOS=0
     totalAndroid=0
     countIOS=0
     countAndroid=0
     totIosAverage=0
     totAndroidAverage=0
     numberOfApps=0
     android_numReviews=0
     ios_numReviews=0

     for post in  collection_ios.find().batch_size(30):
         numberOfApps=numberOfApps+1
         app_title=post['ios_name']
         android_reviews=post['reviews']
         ios_reviews=post['ios_reviews']
         title=post['ios_name']
         print "app name:"+app_title
         print "android_reviews"
         print len(android_reviews)
         print "ios_reviews"
         print len(ios_reviews)
         android_numReviews=android_numReviews+len(android_reviews)
         ios_numReviews=ios_numReviews+len(ios_reviews)





     print "Total iOS reviews:"+str(float(ios_numReviews))
     print "Total Android reviews:"+str(float(android_numReviews))
     print "Total Reviews:"+str(float(android_numReviews)+ios_numReviews)      
     #return collection.find_one()
def count_letters(word):
    return len(word) - word.count(' ')  

if __name__ == '__main__':
    _getCollection()


