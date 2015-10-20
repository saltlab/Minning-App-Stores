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
         android_desc=post['android_description']
         ios_desc=post['ios_description']
         print android_desc
         print "*****IOS****"
         print ios_desc

         print "DONNEE APP"





     print "******** END *************"
   
     #return collection.find_one()
def count_letters(word):
    return len(word) - word.count(' ')  

if __name__ == '__main__':
    _getCollection()


