import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
import os
import errno
from collections import Counter
import operator
from collections import OrderedDict
from operator import itemgetter



#From DB
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_ios=db_ios.matches2kNew


#To DB
client10Android = MongoClient('localhost', 27017)
db_ios10Android=client10Android.Apps 
collection10Android=db_ios10Android.matches10Android

#To DB
client10Ios = MongoClient('localhost', 27017)
db_ios10Ios=client10Ios.Apps 
collection10Ios=db_ios10Ios.matches10Ios 

        
def _getCollection():
     resultList=[]

     for post in  collection_ios.find({'ios_numPD':{'$gte':100},'android_numPD':{'$gte':100}}).batch_size(30):
         android_app_id=post['android_app_id']

         ios_success=(post['ios_success'])
         android_success=post['android_success']

         result={'id':android_app_id,'difference':android_success-ios_success}
         resultList.append(result)

     newlistAndroid = sorted(resultList, key=itemgetter('difference'),reverse=True) 
     newlistIos=sorted(resultList, key=itemgetter('difference')) 

     for i in range(10):
            appId=newlistAndroid[i]['id']
            print appId
            app=collection_ios.find_one({"android_app_id":appId})
            collection10Android.insert_one(app)
     
     for i in range(10):
            appId=newlistIos[i]['id']
            print appId
            app=collection_ios.find_one({"android_app_id":appId})
            collection10Ios.insert_one(app)
if __name__ == '__main__':
    _getCollection()


