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



#From DB
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_ios=db_ios.matches10Ios




        
def _getCollection():
     resultList=[]
     csvfile = "descriptionTopIos.csv"

     for post in  collection_ios.find().batch_size(30):
         ios_description=post['ios_description']
         android_description=post['android_description']
         title=post['ios_name']
         result={'title':title, 'ios_description':ios_description, 'android_description':android_description}
         resultList.append(result)


     #print resultList
     #newlist = sorted(resultList, key=itemgetter('difference'),reverse=True) 
     with open(csvfile, "w") as output:
             writer = csv.writer(output, lineterminator='\n')
             writer.writerow(["title", "ios_description","android_description"])
             for app in resultList:
                title=app['title']
                writer.writerow([title.encode('utf-8').strip(), app['ios_description'].encode('utf-8').strip(), app['android_description'].encode('utf-8').strip()])

if __name__ == '__main__':
    _getCollection()


