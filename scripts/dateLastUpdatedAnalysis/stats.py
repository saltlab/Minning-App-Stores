
import urllib2
from elementtree import ElementTree
import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup
import datetime
import httplib
from datetime import datetime as datetime
import csv


#DB info
client = MongoClient('localhost', 27017)
db=client.Apps 
collection=db.matches80k
csvfile = "341.csv"



def _app_info(language='en_US'):
 count=0
 resultList=[]
 total_number_of_apps=collection.count()

 print "*** Stats 1 ***"
 print "Total Number of Apps: "+str(total_number_of_apps)
 total_number_of_apps_with_updated_date=collection.count({'update_dates':{'$exists':True}})
 print "Number of Apps that have a LAST UPDATED DATE: "+str(total_number_of_apps_with_updated_date)
 percentage=(float(total_number_of_apps_with_updated_date)/total_number_of_apps)*100
 print "percentage of apps with last updated date to all apps:"+str(percentage)+"%"
 #print "*** End of Stats 1 ***"


 countAndroid=0
 countIos=0
 for post in collection.find({'update_dates':{'$exists':True}}):
    update_dates=post['update_dates']
    app_android_updateDate=update_dates['android_updated_date']
    app_ios_updateDate=update_dates['ios_update_date']
    if app_android_updateDate > app_ios_updateDate:
        countAndroid=countAndroid+1

    else:
        countIos=countIos+1
 print "*** Stats 2 ***"      
 print "Number of iOS apps that  are more recently udpated: "+str(countIos)+ " OR "+ str((float(countIos)/total_number_of_apps_with_updated_date)*100)+"%"
 print "Number of Android apps that  are more recently udpated: "+str(countAndroid)+ " OR " +str((float(countAndroid)/total_number_of_apps_with_updated_date)*100)+"%"
 #print "*** End of Stats 2 ***"     
 countAndroid2=0
 countIos2=0

 for post in collection.find({'update_dates':{'$exists':True} ,'$or':[{'update_dates.ios_update_date':{'$gte':datetime(2016,01,01)}}, {'update_dates.android_updated_date':{'$gte':datetime(2016,01,01)}}]},sort=[('update_dates.differenceDays', pymongo.DESCENDING)]):
    count=count+1
    app_name=post['ios_name']
    update_dates=post['update_dates']
    app_android_updateDate=update_dates['android_updated_date']
    app_ios_updateDate=update_dates['ios_update_date']
    if app_android_updateDate > app_ios_updateDate:
        countAndroid2=countAndroid2+1


    else:
        countIos2=countIos2+1
 print "*** Stats 3 ***"      
 print "Number of iOS apps (after 1st of January) that  are more recently udpated: "+str(countIos2)+ " OR "+ str((float(countIos2)/total_number_of_apps_with_updated_date)*100)+"%"
 print "Number of Android (after 1st of January) apps that  are more recently udpated: "+str(countAndroid2)+ " OR " +str((float(countAndroid2)/total_number_of_apps_with_updated_date)*100)+"%"
# print "*** End of Stats 3 ***" 








if __name__ == '__main__':
    #print collection.count({'update_dates':{'$exists':True}, '$or':[{'update_dates.ios_update_date':{'$gte':datetime(2016,01,01)}}, {'update_dates.android_updated_date':{'$gte':datetime(2016,01,01)}}]},sort=[('update_dates.differenceDays', pymongo.DESCENDING)])
    #.sort({'update_dates.differenceDays':-1})
    _app_info()


