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


# #To DB
# client10 = MongoClient('localhost', 27017)
# db_ios10=client10.Apps 
# collection10=db_ios10.matches25

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

    for app in  collection_ios.find().batch_size(30):
        #count=count+1
        #android_rating_total=android_rating_total+float(app['android_ratingsAllVersions'].replace(',',''))
        #ios_rating_total=ios_rating_total+float(app['ios_ratingsAllVersions_new'].replace(',',''))
        android_ratings.append(float(app['android_ratingsAllVersions'].replace(',','')))
        ios_ratings.append(float(app['ios_ratingsAllVersions_new'].replace(',','')))


    android_rating_average=stats.mean(android_ratings)
    ios_rating_average=stats.mean(ios_ratings)

    android_rating_median=stats.median(android_ratings)
    ios_rating_median=stats.median(ios_ratings)

    android_rating_q1=stats.quartiles(android_ratings)[0]
    ios_rating_q1=stats.quartiles(ios_ratings)[0]

    android_rating_q3=stats.quartiles(android_ratings)[1]
    ios_rating_q3=stats.quartiles(ios_ratings)[1]


    print "ios stats"
    print ios_rating_q1
    print ios_rating_median
    print ios_rating_q3
    print "Android stats"
    print android_rating_q1
    print android_rating_median
    print android_rating_q3


        
def _getCollection():
     csvfile = "success.csv"
     apps=[]
     for post in  collection_ios.find().batch_size(30):

         android_app_id=post['android_app_id']
         title=post['ios_name']

         #Reviews
         positiveIos=post['iosSentimentClassifierStats']['positive']
         positiveAndroid=post['androidSentimentClassifierStats']['positive']

         negativeIos=post['iosSentimentClassifierStats']['negative']
         negativeAndroid=post['androidSentimentClassifierStats']['negative']


         problemDiscoveryIos=post['iosOtherClassifierStats']['problemDiscovery']
         problemDiscoveryAndroid=post['androidOtherClassifierStats']['problemDiscovery']

         #Ratings
         android_rating_app=float(post['android_ratingsAllVersions'].replace(',',''))
         ios_rating_app=float(post['ios_ratingsAllVersions_new'].replace(',',''))

         #Stars
         android_star_rating_new=float(post['android_star_rating_new'].replace(',',''))
         ios_starsVersionAllVersions_new=float(post['ios_starsVersionAllVersions_new'].replace(',',''))


         success_android=_sucess_android(positiveAndroid, negativeAndroid, problemDiscoveryAndroid, android_rating_app,android_star_rating_new)
         success_ios=_sucess_ios(positiveIos, negativeIos, problemDiscoveryIos, ios_rating_app,ios_starsVersionAllVersions_new)
         #print success_ios

         #success_android=((float(positiveAndroid)/100)-(float(negativeAndroid)/100)-(float(problemDiscoveryAndroid)/100))+(0.5 if android_rating_total<android_rating_average else 1)+(float(android_star_rating_new)/5)
         #print "success Android:"+ str(success_android)
         #success_ios=((float(positiveIos)/100)-(float(negativeIos)/100)-(float(problemDiscoveryIos)/100)  )+(0.5 if ios_rating_total<ios_rating_average else 1)+(float(ios_starsVersionAllVersions_new)/5)
         #print "success IOS:" +str(success_ios)

         apps.append({'title':title,'android_success':success_android,'problemDiscoveryAndroid':problemDiscoveryAndroid,   'ios_success':success_ios, 'problemDiscoveryIos':problemDiscoveryIos  })
         collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'android_success':success_android, 'ios_success':success_ios}  })

     with open(csvfile, "w") as output:
             writer = csv.writer(output, lineterminator='\n')
             writer.writerow(["title", "Android success","Android PD" ,"Ios Success","Ios PD"])
             for app in apps:
                title=app['title']
                writer.writerow([title.encode('utf-8').strip(), app['android_success'],app['problemDiscoveryAndroid'], app['ios_success'],app['problemDiscoveryIos']])

     # print resultList
     # newlist = sorted(resultList, key=itemgetter('difference'),reverse=True) 
     # print"********"
     # print newlist
     # for item in newlist:
     #    if (item['difference']>25 or item['difference']< -25):
     #        appId=item['id']
     #        print appId
     #        app=collection_ios.find_one({"android_app_id":appId})
     #        collection10.insert_one(app)


def _sucess_android(positiveAndroid, negativeAndroid, problemDiscoveryAndroid, android_rating_app,android_star_rating_new):
         android_reviews=(positiveAndroid+(100-((negativeAndroid+problemDiscoveryAndroid)/2)))/100
         android_stars=android_star_rating_new
         #android_ratings_total=0.25

         #print  "android_rating_app:"+str(android_rating_app)
         #print  "android_rating_q1:"+str(android_rating_q1)
         if (android_rating_app<android_rating_q1): 
            android_ratings_total=0.25
         elif ((android_rating_app>android_rating_q1) and (android_rating_app<android_rating_median)):
            android_ratings_total=0.5 

         elif((android_rating_app>android_rating_median) and (android_rating_app<android_rating_q3) ):
            android_ratings_total=0.75 

         else:
            android_ratings_total=1
         #print android_ratings_total

         success_android=((android_reviews+(android_stars*android_ratings_total))/7)*100
         return success_android
def _sucess_ios(positiveIos, negativeIos, problemDiscoveryIos, ios_rating_app,ios_starsVersionAllVersions_new):
         ios_reviews=(positiveIos+(100-((negativeIos+problemDiscoveryIos)/2)))/100
         ios_stars=ios_starsVersionAllVersions_new

         if (ios_rating_app<ios_rating_q1): 
            ios_ratings_total=0.25
         elif ((ios_rating_app>ios_rating_q1) and (ios_rating_app<ios_rating_median)):
            ios_ratings_total=0.5 

         elif((ios_rating_app>ios_rating_median) and (ios_rating_app<ios_rating_q3) ):
            ios_ratings_total=0.75 

         else:
            ios_ratings_total=1
         #print ios_ratings_total

         success_ios=((ios_reviews+(ios_stars*ios_ratings_total))/7)*100
         return success_ios             
if __name__ == '__main__':
    _getRatingAverages()

    _getCollection()


