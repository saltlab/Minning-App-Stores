 #!/usr/bin/env python
''' Apple AppStore reviews scrapper
    version 2011-04-12
    Tomek "Grych" Gryszkiewicz, grych@tg.pl
    http://www.tg.pl
    
    based on "Scraping AppStore Reviews" blog by Erica Sadun
     - http://blogs.oreilly.com/iphone/2008/08/scraping-appstore-reviews.html
    AppStore codes are based on "appstore_reviews" by Jeremy Wohl
     - https://github.com/jeremywohl/iphone-scripts/blob/master/appstore_reviews
'''
import urllib2
from elementtree import ElementTree
import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
import os
import errno

appStores = {

'United States':      143441
}
#IOS DB info
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_ios=db_ios.matchesTestReviews

#android DB info
client_android = MongoClient('localhost', 27017)
db_android=client_android.Apps 
collection_android=db_android.androidAppsPilot

        
def _getCollection():
     apps=[]
     for post in  collection_ios.find().batch_size(30):
         android_reviews=post['reviews']
         ios_reviews=post['ios_reviews']
         #create directory for each app
         make_sure_path_exists("reviews/"+post['android_title']+"/"+"iosReviews")
         make_sure_path_exists("reviews/"+post['android_title']+"/"+"androidReviews")
         
         android_directory="reviews/"+post['android_title']+"/"+"androidReviews"
         ios_directory="reviews/"+post['android_title']+"/"+"iosReviews"
         app_title=post['android_title']
         #pass the reviews to this methods and dump reviews as txt files in corresponding categories
         conver2txt(android_directory,ios_directory,ios_reviews,android_reviews,app_title)

   
     #return collection.find_one()
def conver2txt(android_directory,ios_directory,ios_reviews,android_reviews,app_title):
     #android_file=open(android_directory+"/reviews.txt", "a")
     #ios_file = open(ios_directory+"/reviews.txt", "a")
     number=0
     for review in ios_reviews:
        number += 1
        temp_file=open(ios_directory+"/iOS"+app_title+"reviews"+str(number)+".txt", "w")
        temp_file.write(review['topic'].encode('utf-8').strip())
        temp_file.write("\n")
        temp_file.write(review['review'].encode('utf-8').strip())

     number_android=0
     for review_android in android_reviews:
        number_android +=1
        temp_file_android=open(android_directory+"/Android"+app_title+"reviews"+str(number_android)+".txt", "w")
        #temp_file_android.write(review_android['reviewTitle'].encode('utf-8').strip())
        temp_file_android.write("\n")
        temp_file_android.write(review_android['reviewBody'].encode('utf-8').strip())

        
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__ == '__main__':

   _getCollection()


