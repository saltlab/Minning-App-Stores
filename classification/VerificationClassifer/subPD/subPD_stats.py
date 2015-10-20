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
collection_ios=db_ios.matches2kNew

        
def _getCollection():
     csvfile = "subPDAll.csv"
     results=[]
     for post in  collection_ios.find({'androidSubPDClassifierStats':{'$exists':True}}).batch_size(30):
         app_title=post['ios_name']
         iosSubPD=post['iosSubPDClassifierStats']
         androidSubPD=post['androidSubPDClassifierStats']

         ios_postUpdate=iosSubPD['postUpdate']
         ios_moneyComplaints=iosSubPD['moneyComplaints']
         ios_critical=iosSubPD['critical']
         ios_other=iosSubPD['other']
         ios_appFeature=iosSubPD['appFeature']

         android_postUpdate=androidSubPD['postUpdate']
         android_moneyComplaints=androidSubPD['moneyComplaints']
         android_critical=androidSubPD['critical']
         android_other=androidSubPD['other']
         android_appFeature=androidSubPD['appFeature']
         results.append({'title':app_title, 'ios_critical':ios_critical,'android_critical':android_critical, 
                                            'ios_moneyComplaints':ios_moneyComplaints,'android_moneyComplaints':android_moneyComplaints,
                                            'ios_appFeature':ios_appFeature, 'android_appFeature':android_appFeature,
                                            'ios_postUpdate':ios_postUpdate, 'android_postUpdate':android_postUpdate,
                                            'ios_other':ios_other, 'android_other':android_other})

     with open(csvfile, "w") as output:
             writer = csv.writer(output, lineterminator='\n')
             writer.writerow(["title", "ios_critical","android_critical" ,"ios_moneyComplaints","android_moneyComplaints","ios_appFeature","android_appFeature","ios_postUpdate","android_postUpdate","ios_other","android_other"])
             for app in results:
                title=app['title']
                writer.writerow([title.encode('utf-8').strip(), app['ios_critical'],app['android_critical'], app['ios_moneyComplaints'],app['android_moneyComplaints'],app['ios_appFeature'],app['android_appFeature'], app['ios_postUpdate'],app['android_postUpdate'],app['ios_other'],app['android_other']     ])


if __name__ == '__main__':
    _getCollection()


