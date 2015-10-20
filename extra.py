
import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
import os
import errno
import csv


#IOS DB info
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection=db_ios.matches80k


        
def _getCollectionAndroid():
     android_zero=0
     ios_zero=0
     #Loop through to get stats on Android Category vs Price
     for post in  collection.find({'updated':True}).batch_size(30):
         android_app_id=post['android_app_id']
         android_stars=post['android_star_rating_new']
         ios_stars=post['ios_starsVersionAllVersions_new']
         

         if(android_stars=='0.0'):
          collection.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'android_isZeroStars':'true'}  })
         if(ios_stars=='0.0'):
          collection.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'ios_isZeroStars':'true'}  })
     print android_zero
     print ios_zero       

       

if __name__ == '__main__':

   _getCollectionAndroid()



