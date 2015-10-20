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


#To Andriod DB
client10Android = MongoClient('localhost', 27017)
db_ios10Android=client10Android.Apps 
collection10Android=db_ios10Android.zAndroid

#To iOS DB
client10Ios = MongoClient('localhost', 27017)
db_ios10Ios=client10Ios.Apps 
collection10Ios=db_ios10Ios.zIos 

#To Equal DB
client10Equal = MongoClient('localhost', 27017)
db_ios10Equal=client10Equal.Apps 
collection10Equal=db_ios10Equal.zEqual



android_rating_average=0
ios_rating_average=0

android_rating_median=0
ios_rating_median=0

android_rating_q1=0
ios_rating_q1=0

android_rating_q3=0
ios_rating_q3=0

def _getRatingAverages():
    count=0
    android_rating_total=0
    ios_rating_total=0
    android_ratings=[]
    ios_ratings=[]

    global android_rating_average
    global ios_rating_average

    global android_rating_median
    global ios_rating_median

    global android_rating_q1
    global ios_rating_q1

    global android_rating_q3
    global ios_rating_q3

    for app in  collection_ios.find(no_cursor_timeout=True):
        #count=count+1
        #android_rating_total=android_rating_total+float(app['android_ratingsAllVersions'].replace(',',''))
        #ios_rating_total=ios_rating_total+float(app['ios_ratingsAllVersions_new'].replace(',',''))
        android_ratings.append(float(app['android_success']-app['ios_success']))
        #ios_ratings.append(float(app['ios_success']))
        #difference


    android_rating_average=stats.mean(android_ratings)
    #ios_rating_average=stats.mean(ios_ratings)

    android_rating_median=stats.median(android_ratings)
    #ios_rating_median=stats.median(ios_ratings)

    android_rating_q1=stats.quartiles(android_ratings)[0]
    #ios_rating_q1=stats.quartiles(ios_ratings)[0]

    android_rating_q3=stats.quartiles(android_ratings)[1]
    #ios_rating_q3=stats.quartiles(ios_ratings)[1]

    print "Android stats"
    print android_rating_q1
    print android_rating_median
    print android_rating_q3

def _getCollection():
    androidBetter=[]
    iosBetter=[]
    equal=[]
    for app in collection_ios.find(no_cursor_timeout=True):
        #print "hello"
        android_success=app['android_success']
        ios_success=app['ios_success']
        app_id=app['android_app_id']
        difference=android_success - ios_success
        if difference<android_rating_q1:
            iosBetter.append(app_id)
        elif difference>android_rating_q1 and difference<android_rating_q3:
            equal.append(app_id)
        else:
            androidBetter.append(app_id)


    print "size ios:"+str(len(iosBetter))
    print "size qual:"+str(len(equal))
    print "size android:"+str(len(androidBetter))
    for result in iosBetter:
        retrievedApp=collection_ios.find_one({"android_app_id":result})
        collection10Ios.insert_one(retrievedApp)
        #print result

    for result in equal:
        retrievedApp=collection_ios.find_one({"android_app_id":result})
        collection10Equal.insert_one(retrievedApp)
    
    for result in androidBetter:
        retrievedApp=collection_ios.find_one({"android_app_id":result})
        collection10Android.insert_one(retrievedApp)        
        
           
if __name__ == '__main__':
    _getRatingAverages()
    _getCollection()



