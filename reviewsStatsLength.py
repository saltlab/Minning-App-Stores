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
     for post in  collection_ios.find().batch_size(30):
         numberOfApps=numberOfApps+1
         android_reviews=post['reviews']
         ios_reviews=post['ios_reviews']
         title=post['ios_name']
         #create directory for each app
         for review in ios_reviews:
            countIOS=countIOS+1
            totalIOS=totalIOS+count_letters(review['topic']+review['review'])
         
         #print title+":"
         totIosAverage=totIosAverage+float(totalIOS/countIOS)


         for reviewAndroid in android_reviews:
            countAndroid=countAndroid+1
            totalAndroid=totalAndroid+count_letters(reviewAndroid['reviewBody'])

         totAndroidAverage=totAndroidAverage+float(totalAndroid/countAndroid)
         print "*************************"

     print "Average length ios:"+str(float(totIosAverage)/numberOfApps)
     print "Average length Android:"+str(float(totAndroidAverage)/numberOfApps)      
     #return collection.find_one()
def count_letters(word):
    return len(word) - word.count(' ')  

if __name__ == '__main__':
    _getCollection()


