
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
     csvfile = "androidCategoryStars.csv"
     categorysVisited=[]
     categoryPrice=[]
     #Loop through to get stats on Android Category vs Price
     for post in  collection.find({'updated':True}).batch_size(30):
         android_category=post['android_category']

         if android_category not in categorysVisited:
            categorysVisited.append(android_category)
            counter=0
            prices=0
            for app in collection.find({'android_category':android_category,'android_star_rating_new':{'$exists':True},'android_isZeroStars':{'$exists':False}}):
                counter=counter+1
                #print android_category
                prices=prices+float(app['android_star_rating_new'].replace(',',''))

            AveragePrice=float(prices)/counter
            categoryPrice.append({'category':android_category,'Apps in Category':counter,'Avg Stars':AveragePrice})

     print categoryPrice
     with open(csvfile, "w") as output:
             writer = csv.writer(output, lineterminator='\n')
             writer.writerow(["Categorys", "Number of Apps in Cateogry","Avg Stars"])
             for category in categoryPrice:
                category_name=category['category']
                writer.writerow([category_name.encode('utf-8').strip(), category['Apps in Category'], category['Avg Stars']])  
def _getCollectionIOS():
     csvfile2 = "iOSCategoryStars.csv"
     categorysVisited=[]
     categoryPrice=[]
     #Loop through to get stats on Android Category vs Price
     for post in  collection.find({'updated':True}).batch_size(30):
         ios_category=post['ios_category']

         if ios_category not in categorysVisited:
            categorysVisited.append(ios_category)
            counter=0
            prices=0
            for app in collection.find({'ios_category':ios_category,'ios_starsVersionAllVersions_new':{'$exists':True},'ios_isZeroStars':{'$exists':False}}):
                counter=counter+1
                #print android_category
                prices=prices+float(app['ios_starsVersionAllVersions_new'].replace(',',''))

            AveragePrice=float(prices)/counter
            categoryPrice.append({'category':ios_category,'Apps in Category':counter,'Avg Stars':AveragePrice})

     print categoryPrice
     with open(csvfile2, "w") as output:
             writer = csv.writer(output, lineterminator='\n')
             writer.writerow(["Categorys", "Number of Apps in Cateogry","Avg Stars"])
             for category in categoryPrice:
                category_name=category['category']
                writer.writerow([category_name.encode('utf-8').strip(), category['Apps in Category'], category['Avg Stars']])                       

if __name__ == '__main__':

   _getCollectionAndroid()
   _getCollectionIOS()


