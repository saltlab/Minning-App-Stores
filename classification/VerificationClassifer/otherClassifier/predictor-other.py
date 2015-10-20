"""Build a sentiment analysis / polarity model

Sentiment analysis can be casted as a binary text classification problem,
that is fitting a linear classifier on features extracted from the text
of the user messages so as to guess wether the opinion of the author is
positive or negative.

In this examples we will use a movie review dataset.

"""
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

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
collection_ios=db_ios.matches2kNew

def _getCollectionIOS():
    count=0
    And_numberPosReviews=0
    And_numberNegReviews=0
    And_numberNeutReviews=0
    numberApps=0
    totalAvgPos=0
    totalAvgNeg=0
    totalAvgNet=0
    # the training data folder must be passed as first argument
    movie_reviews_data_folder = sys.argv[1]
    dataset = load_files(movie_reviews_data_folder, shuffle=False)

    for post in  collection_ios.find().batch_size(30):
            count=count+1
            #print count
            numberApps=numberApps+1
            And_numberPosReviews=0
            And_numberNegReviews=0
            And_numberNeutReviews=0
            numberOfReviews=0
            #android_reviews=post['reviews']
            ios_reviews=post['ios_reviews']
            app_name=post['ios_name']
            android_app_id=post['android_app_id']
            PD_reviews=[]
            # Predict the result on some short new sentences:
        #if app_name=="Vine":
            sentences = [
           
            ]

            for review in ios_reviews:
                sentences.append(review['topic']+" "+review['review'])
                #sentences.append(review['reviewBody'])
            #pickle.loads(saved_classifier)
            restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')


            predicted = restored_classifier.predict(sentences)

            for s, p in zip(sentences, predicted):
             if p==0:
                And_numberPosReviews=And_numberPosReviews+1
                PD_reviews.append(s)
                #print s
             elif p==1:
                And_numberNegReviews=And_numberNegReviews+1
             else:
                And_numberNeutReviews=And_numberNeutReviews+1      
                #print(u'The sentiment of "%s" is "%s"' % (s, dataset.target_names[p]))

            #print "App Name:"+app_name 
            numberOfReviews=len(sentences)
            #print "number of reviews:"+str(len(sentences))
            #print "positive Reviews:"+str((float(And_numberPosReviews)/numberOfReviews)*100)+"%"
            problemDiscovery=(float(And_numberPosReviews)/numberOfReviews)*100

            #print "negative Reviews:"+str((float(And_numberNegReviews)/numberOfReviews)*100)+"%"
            feautreRequest=(float(And_numberNegReviews)/numberOfReviews)*100
            #print "neutral Reviews:"+str((float(And_numberNeutReviews)/numberOfReviews)*100)+"%"
            nonInformative=(float(And_numberNeutReviews)/numberOfReviews)*100
            iosOtherClassifierStats={'problemDiscovery':problemDiscovery,'feautreRequest':feautreRequest,'nonInformative':nonInformative}
            collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'ios_PDReviews':PD_reviews,   'iosOtherClassifierStats':iosOtherClassifierStats,'ios_numPD':And_numberPosReviews}  })



            totalAvgPos=totalAvgPos+(float(And_numberPosReviews)/numberOfReviews)*100
            totalAvgNeg=totalAvgNeg+(float(And_numberNegReviews)/numberOfReviews)*100
            totalAvgNet=totalAvgNet+(float(And_numberNeutReviews)/numberOfReviews)*100
            #print "****************************"


    print "Average problem discovery reviews:"+str(totalAvgPos/numberApps)
    print "Average feautre request reviews:"+str(totalAvgNeg/numberApps)  
    print "Average non-informative reviews:"+str(totalAvgNet/numberApps)



def _getCollectionAndroid():

    And_numberPosReviews=0
    And_numberNegReviews=0
    And_numberNeutReviews=0
    numberApps=0
    totalAvgPos=0
    totalAvgNeg=0
    totalAvgNet=0
    count=0
    # the training data folder must be passed as first argument
    movie_reviews_data_folder = sys.argv[1]
    dataset = load_files(movie_reviews_data_folder, shuffle=False)

    for post in  collection_ios.find().batch_size(30):
            count=count+1
            #print count
            numberApps=numberApps+1
            And_numberPosReviews=0
            And_numberNegReviews=0
            And_numberNeutReviews=0
            numberOfReviews=0
            android_reviews=post['reviews']
            #ios_reviews=post['ios_reviews']
            app_name=post['ios_name']
            android_app_id=post['android_app_id']
            # Predict the result on some short new sentences:
        #if app_name=="Vine":
            PD_reviews=[]
            sentences = [
           
            ]

            for review in android_reviews:
                #sentences.append(review['topic']+" "+review['review'])
                sentences.append(review['reviewBody'])
            #pickle.loads(saved_classifier)
            restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')


            predicted = restored_classifier.predict(sentences)

            for s, p in zip(sentences, predicted):
             if p==0:
                And_numberPosReviews=And_numberPosReviews+1
                PD_reviews.append(s)
             elif p==1:
                And_numberNegReviews=And_numberNegReviews+1
             else:
                And_numberNeutReviews=And_numberNeutReviews+1      
                #print(u'The sentiment of "%s" is "%s"' % (s, dataset.target_names[p]))

            #print "App Name:"+app_name 
            numberOfReviews=len(sentences)
            #print "number of reviews:"+str(len(sentences))
            #print "positive Reviews:"+str((float(And_numberPosReviews)/numberOfReviews)*100)+"%"
            problemDiscovery=(float(And_numberPosReviews)/numberOfReviews)*100

            #print "negative Reviews:"+str((float(And_numberNegReviews)/numberOfReviews)*100)+"%"
            feautreRequest=(float(And_numberNegReviews)/numberOfReviews)*100
            #print "neutral Reviews:"+str((float(And_numberNeutReviews)/numberOfReviews)*100)+"%"
            nonInformative=(float(And_numberNeutReviews)/numberOfReviews)*100
            iosOtherClassifierStats={'problemDiscovery':problemDiscovery,'feautreRequest':feautreRequest,'nonInformative':nonInformative}
            collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'android_PDReviews':PD_reviews,   'androidOtherClassifierStats':iosOtherClassifierStats, 'android_numPD':And_numberPosReviews}  })



            totalAvgPos=totalAvgPos+(float(And_numberPosReviews)/numberOfReviews)*100
            totalAvgNeg=totalAvgNeg+(float(And_numberNegReviews)/numberOfReviews)*100
            totalAvgNet=totalAvgNet+(float(And_numberNeutReviews)/numberOfReviews)*100
            #print "****************************"


    print "Average problem discovery reviews:"+str(totalAvgPos/numberApps)
    print "Average feautre request reviews:"+str(totalAvgNeg/numberApps)  
    print "Average non-informative reviews:"+str(totalAvgNet/numberApps)    

if __name__ == '__main__':
   print "ios stats:"
   _getCollectionIOS()
   print("********************") 
   print "android stats:"
   _getCollectionAndroid()             
          

