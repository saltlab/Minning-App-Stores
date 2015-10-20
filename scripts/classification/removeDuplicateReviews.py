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
import csv
import stats


#From DB
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_ios=db_ios.matches2kNew

        
def _getCollection():
    count=0

    for post in  collection_ios.find().batch_size(30):
         count=count+1
         print count
         android_app_id=post['android_app_id']
         title=post['ios_name']
         android_reviews=post['reviews']
         reviews_old=[]

         for review in android_reviews:
            reviews_old.append(review['reviewBody'])

         #print type(reviews_old[1])
         android_reviews_noDuplicates=list(set(reviews_old))
         reviews_new=[]
         for review_new in android_reviews_noDuplicates:
            reviews_new.append({"reviewBody":review_new})
         #print reviews_new   

         collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'reviews':reviews_new}  })

           
if __name__ == '__main__':

    _getCollection()


