import sys
import pickle

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
     for post in  collection_ios.find().batch_size(30):
         android_reviews=post['reviews']
         ios_reviews=post['ios_reviews']
         android_app_id=post['android_app_id']
         lenAndroid=len(android_reviews)
         lenIOS=len(ios_reviews)

         if(lenIOS>lenAndroid):
            difference=lenIOS-lenAndroid
            #print difference
            ios_reviews_new=ios_reviews[0:lenIOS-difference]
            #print len(ios_reviews_new)
            collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'ios_reviews':ios_reviews_new}  })

         elif(lenAndroid>lenIOS):
           difference=lenAndroid-lenIOS
           #print difference
           android_reviews_new=android_reviews[0:lenAndroid-difference]
           #print len(android_reviews_new)
           collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'reviews':android_reviews_new}  })
               

   

if __name__ == '__main__':

   _getCollection()


