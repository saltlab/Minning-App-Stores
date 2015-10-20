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
client10 = MongoClient('localhost', 27017)
db_ios10=client10.Apps 
collection10=db_ios10.matches25

        
def _getCollection():
     resultList=[]

     for post in  collection_ios.find().batch_size(30):
         iosOtherClassifierStats=post['iosOtherClassifierStats']
         androidOtherClassifierStats=post['androidOtherClassifierStats']
         android_app_id=post['android_app_id']

         problemDiscoveryIos=(iosOtherClassifierStats['problemDiscovery'])
         problemDiscoveryAndroid=androidOtherClassifierStats['problemDiscovery']

         result={'id':android_app_id,'difference':problemDiscoveryAndroid-problemDiscoveryIos}
         resultList.append(result)


     print resultList
     newlist = sorted(resultList, key=itemgetter('difference'),reverse=True) 
     print"********"
     print newlist
     for item in newlist:
        if (item['difference']>25 or item['difference']< -25):
            appId=item['id']
            print appId
            app=collection_ios.find_one({"android_app_id":appId})
            collection10.insert_one(app)

if __name__ == '__main__':
    _getCollection()


