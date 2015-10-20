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
collection_ios=db_ios.matches2kNew




        
def _getCollection():
     resultList=[]
     csvfile = "rankingAll.csv"

     for post in  collection_ios.find().batch_size(30):
         iosSentimentClassifierStats=post['iosSentimentClassifierStats']
         androidSentimentClassifierStats=post['androidSentimentClassifierStats']

         iosOtherClassifierStats=post['iosOtherClassifierStats']
         androidOtherClassifierStats=post['androidOtherClassifierStats']
         android_app_id=post['android_app_id']
         title=post['ios_name']

         #Positive
         positiveIos=(iosSentimentClassifierStats['positive'])
         positiveAndroid=androidSentimentClassifierStats['positive']

         #Negative
         negativeIos=(iosSentimentClassifierStats['negative'])
         negativeAndroid=androidSentimentClassifierStats['negative']

         #Neutral
         neutralIos=(iosSentimentClassifierStats['neautral'])
         neutralAndroid=androidSentimentClassifierStats['neautral']

         #Problem Discovery
         problemDiscoveryIos=(iosOtherClassifierStats['problemDiscovery'])
         problemDiscoveryAndroid=androidOtherClassifierStats['problemDiscovery']

         #Feautre Request
         featureRequestIos=(iosOtherClassifierStats['feautreRequest'])
         featureRequestAndroid=androidOtherClassifierStats['feautreRequest']

         #Non-informative
         nonInfoIos=(iosOtherClassifierStats['nonInformative'])
         nonInfoAndroid=androidOtherClassifierStats['nonInformative']

         #Success
         successIos=(post['ios_success'])
         successAndroid=post['android_success']

         result={'title':title, 'id':android_app_id,'positiveIos':positiveIos
                                                   ,'positiveAndroid':positiveAndroid 
                                                    ,'negativeIos':negativeIos 
                                                    ,'negativeAndroid':negativeAndroid 
                                                    ,'neutralIos':neutralIos 
                                                    ,'neutralAndroid':neutralAndroid 
                                                    ,'problemDiscoveryIos':problemDiscoveryIos 
                                                    ,'problemDiscoveryAndroid':problemDiscoveryAndroid 
                                                    ,'featureRequestIos':featureRequestIos 
                                                    ,'featureRequestAndroid':featureRequestAndroid 
                                                    ,'nonInfoIos':nonInfoIos 
                                                    ,'nonInfoAndroid':nonInfoAndroid 
                                                    ,'successIos':successIos
                                                    ,'successAndroid':successAndroid}
         resultList.append(result)


     #print resultList
     #newlist = sorted(resultList, key=itemgetter('difference'),reverse=True) 
     with open(csvfile, "w") as output:
             writer = csv.writer(output, lineterminator='\n')
             writer.writerow(["title", "positiveIos","positiveAndroid","negativeIos","negativeAndroid","neutralIos","neutralAndroid","problemDiscoveryIos","problemDiscoveryAndroid","featureRequestIos","featureRequestAndroid","nonInfoIos","nonInfoAndroid","successIos","successAndroid"    ])
             for app in resultList:
                title=app['title']
                writer.writerow([title.encode('utf-8').strip(), app['positiveIos'], app['positiveAndroid'], app['negativeIos'],app['negativeAndroid'], app['neutralIos'], app['neutralAndroid'],app['problemDiscoveryIos'], app['problemDiscoveryAndroid'], app['featureRequestIos'],app['featureRequestAndroid'], app['nonInfoIos'], app['nonInfoAndroid'],app['successIos'],app['successAndroid']])

if __name__ == '__main__':
    _getCollection()


