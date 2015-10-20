import sys
import pickle

from sklearn.externals import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import sys
import string
import argparse
import re
import json
import pymongo
from pymongo import MongoClient
import os
import errno
#IOS DB info
client_ios = MongoClient('localhost', 27017)
db_ios=client_ios.Apps 
collection_ios=db_ios.matches10Ios


        
def _getCollection():
     # the training data folder must be passed as first argument
     movie_reviews_data_folder = sys.argv[1]
     dataset = load_files(movie_reviews_data_folder, shuffle=False)
     #apps=[]
     for post in  collection_ios.find().batch_size(30):
         android_reviews=post['reviews']
         ios_reviews=post['ios_reviews']
         #create directory for each app
         make_sure_path_exists("PDreviews/"+post['android_title']+"/"+"iosReviews")
         make_sure_path_exists("PDreviews/"+post['android_title']+"/"+"androidReviews")
         
         android_directory="PDreviews/"+post['android_title']+"/"+"androidReviews"
         ios_directory="PDreviews/"+post['android_title']+"/"+"iosReviews"
         app_title=post['android_title']
         #pass the reviews to this methods and dump reviews as txt files in corresponding categories
         conver2txt(android_directory,ios_directory,ios_reviews,android_reviews,app_title)

   
     #return collection.find_one()
def conver2txt(android_directory,ios_directory,ios_reviews,android_reviews,app_title):
     #android_file=open(android_directory+"/reviews.txt", "a")
     #ios_file = open(ios_directory+"/reviews.txt", "a")
    number=0
    sentencesIos = [
           
        ]
    sentencesAndroid = [
           
        ]
    for review in ios_reviews:
        sentencesIos.append(review['topic']+" "+review['review'])
     
    restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')
    predicted = restored_classifier.predict(sentencesIos)
    for s, p in zip(sentencesIos, predicted):
        if p==0:
            #print s
            number += 1
            temp_file=open(ios_directory+"/iOS"+app_title+"reviews"+str(number)+".txt", "w")
            #temp_file.write(review['topic'].encode('utf-8').strip())
            temp_file.write("\n")
            temp_file.write(s.encode('utf-8').strip())

       

    number_android=0
    for review_android in android_reviews:
        sentencesAndroid.append(review_android['reviewBody'])

    restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')
    predicted = restored_classifier.predict(sentencesAndroid)
    for s, p in zip(sentencesAndroid, predicted):
        if p==0:
            number_android +=1
            temp_file_android=open(android_directory+"/Android"+app_title+"reviews"+str(number_android)+".txt", "w")
            #temp_file_android.write(review_android['reviewTitle'].encode('utf-8').strip())
            temp_file_android.write("\n")
            temp_file_android.write(s.encode('utf-8').strip())
      



        

        
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

if __name__ == '__main__':

   _getCollection()


