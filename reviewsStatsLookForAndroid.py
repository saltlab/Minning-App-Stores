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
collection_ios=db_ios.matches2kNew

        
def _getCollection():
     apps=[]
     totalIOS=0
     totalAndroid=0
     countIOS=0
     countAndroid=0
     totIosAverage=0
     totAndroidAverage=0
     numberOfApps=0
     stringsToSearch=['android','samsung','galaxy']
     for post in  collection_ios.find().batch_size(30):
         numberOfApps=numberOfApps+1
         android_reviews=post['reviews']
         ios_reviews=post['ios_reviews']
         title=post['ios_name']
         url=post['ios_url']
         #create directory for each app
         for review in ios_reviews:
            countIOS=countIOS+1
            totalIOS=(review['topic']+review['review'])
            for string in stringsToSearch:
                searhKey=string
                if (totalIOS.find(searhKey)) > -1:
                    print title
                    print url
                    print totalIOS
                    print "*******************"
         


if __name__ == '__main__':
    _getCollection()


