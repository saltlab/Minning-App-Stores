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
collection_ios=db_ios.matchesTestReviews

if __name__ == "__main__":

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

    #problem Discovery variables
    problemDiscoveryTP=0
    problemDiscoveryFP=0
    problemDiscoveryFN=0

    #Feature Request variables
    featureRequestTP=0
    featureRequestFP=0
    featureRequestFN=0

    #non-informative variables
    nonInformativeTP=0
    nonInformativeFP=0
    nonInformativeFN=0

    # Read the reviews that need to be verified
    path = '/Users/mohamedali/Minning-App-Stores/classification/verifyClassifiersData/2-genericClassifier/1-ProblemDiscovery'  # remove the trailing '\'
    problemDiscovery = []
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                #problemDiscovery[dir_entry] = my_file.read()
                problemDiscovery.append(my_file.read())



    path = '/Users/mohamedali/Minning-App-Stores/classification/verifyClassifiersData/2-genericClassifier/2-FeatureRequest'  # remove the trailing '\'
    featureRequest = []
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                #featureRequest[dir_entry] = my_file.read()
                featureRequest.append(my_file.read())

    path = '/Users/mohamedali/Minning-App-Stores/classification/verifyClassifiersData/2-genericClassifier/3-NonInformative'  # remove the trailing '\'
    nonInformative = []
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                #nonInformative[dir_entry] = my_file.read()
                nonInformative.append(my_file.read())


    print len (problemDiscovery)
    print len (featureRequest)        
    print len (nonInformative)
    restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')
    predicted = restored_classifier.predict(problemDiscovery)
    for s, p in zip(problemDiscovery, predicted):
        #print(u'The sentiment of "%s" is "%s"' % (s, dataset.target_names[p]))
        if p==0: #problem discovery
            problemDiscoveryTP=problemDiscoveryTP+1
        elif p==1: #feature request
            problemDiscoveryFP=problemDiscoveryFP+1
            featureRequestFN=featureRequestFN+1
        else:#non-informative
            problemDiscoveryFP=problemDiscoveryFP+1 
            nonInformativeFN=nonInformativeFN+1


    restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')
    predicted = restored_classifier.predict(featureRequest)
    for s, p in zip(featureRequest, predicted):
        #print(u'The sentiment of "%s" is "%s"' % (s, dataset.target_names[p]))
        if p==0: #problem discovery
            featureRequestFP=featureRequestFP+1
            problemDiscoveryFN=problemDiscoveryFN+1
        elif p==1: #feature request
            featureRequestTP=featureRequestTP+1  
        else:#non-informative
            featureRequestFP=featureRequestFP+1
            nonInformativeFN=nonInformativeFN+1
 

    restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')
    predicted = restored_classifier.predict(nonInformative)
    for s, p in zip(nonInformative, predicted):
        #print(u'The sentiment of "%s" is "%s"' % (s, dataset.target_names[p]))
        if p==0: #problem discovery
            nonInformativeFP=nonInformativeFP+1
            problemDiscoveryFN=problemDiscoveryFN+1
        elif p==1: #feature request
            nonInformativeFP=nonInformativeFP+1
            featureRequestFN=featureRequestFN+1

        else:#non-informative
            nonInformativeTP=nonInformativeTP+1 
                      
    print "TP"+str(featureRequestTP)
    print "FP"+str(problemDiscoveryFP)
    print "FN"+str(problemDiscoveryFN)
    problemDiscoveryPrecision=(float(problemDiscoveryTP)/(problemDiscoveryTP+problemDiscoveryFP))
    problemDiscoveryRecall=(float(problemDiscoveryTP)/(problemDiscoveryTP+problemDiscoveryFN))
    problemDiscoveryFmeasure=(float(2*problemDiscoveryPrecision*problemDiscoveryRecall)/(problemDiscoveryPrecision+problemDiscoveryRecall))
    print "Problem Discovery Precision:"+str(problemDiscoveryPrecision)
    print "Problem Discovery Recall:"+str(problemDiscoveryRecall)
    print "Problem Discovery F-measure:"+str(problemDiscoveryFmeasure)
    print "********"


    featureRequestPrecision=(float(featureRequestTP)/(featureRequestTP+featureRequestFP))
    featureRequestRecall=(float(featureRequestTP)/(featureRequestTP+featureRequestFN))
    featureRequestFmeasure=(float(2*featureRequestPrecision*featureRequestRecall)/(featureRequestPrecision+featureRequestRecall))
    print "Feature Request Precision:"+str(featureRequestPrecision)
    print "Feature Request Recall:"+str(featureRequestRecall)
    print "Feature Request F-measure:"+str(featureRequestFmeasure)
    print "********"

    nonInformativePrecision=(float(nonInformativeTP)/(nonInformativeTP+nonInformativeFP))
    nonInformativeRecall=(float(nonInformativeTP)/(nonInformativeTP+nonInformativeFN))
    nonInformativeFmeasure=(float(2*nonInformativePrecision*nonInformativeRecall)/(nonInformativePrecision+nonInformativeRecall))
    print "non-informative Precision:"+str(nonInformativePrecision)
    print "non-informative Recall:"+str(nonInformativeRecall)
    print "non-informative F-measure:"+str(nonInformativeFmeasure)
    print "********"


                    
    # for post in  collection_ios.find().batch_size(30):
    #         numberApps=numberApps+1
    #         And_numberPosReviews=0
    #         And_numberNegReviews=0
    #         And_numberNeutReviews=0
    #         numberOfReviews=0
    #         android_reviews=post['reviews']
    #         #ios_reviews=post['ios_reviews']
    #         app_name=post['ios_name']
    #         # Predict the result on some short new sentences:
    #     #if app_name=="Vine":
    #         sentences = [
           
    #         ]

    #         for review in android_reviews:
    #             #sentences.append(review['topic']+" "+review['review'])
    #             sentences.append(review['reviewBody'])
    #         #pickle.loads(saved_classifier)
    #         restored_classifier = joblib.load('OtherClassifier7Apps/mysentiment-classifier.pkl')
    #         predicted = restored_classifier.predict(sentences)

    #         #print(predicted)

    #         for s, p in zip(sentences, predicted):
    #          if p==0:
    #             And_numberPosReviews=And_numberPosReviews+1
    #          elif p==1:
    #             And_numberNegReviews=And_numberNegReviews+1
    #          else:
    #             And_numberNeutReviews=And_numberNeutReviews+1      
                #print(u'The sentiment of "%s" is "%s"' % (s, dataset.target_names[p]))


    #         print "App Name:"+app_name 
    #         numberOfReviews=len(sentences)
    #         print "number of reviews:"+str(len(sentences))
    #         print "positive Reviews:"+str((float(And_numberPosReviews)/numberOfReviews)*100)+"%"
    #         print "negative Reviews:"+str((float(And_numberNegReviews)/numberOfReviews)*100)+"%"
    #         print "neutral Reviews:"+str((float(And_numberNeutReviews)/numberOfReviews)*100)+"%"
    #         totalAvgPos=totalAvgPos+(float(And_numberPosReviews)/numberOfReviews)*100
    #         totalAvgNeg=totalAvgNeg+(float(And_numberNegReviews)/numberOfReviews)*100
    #         totalAvgNet=totalAvgNet+(float(And_numberNeutReviews)/numberOfReviews)*100
    #         print "****************************"
    # print "Average pos reviews:"+str(totalAvgPos/numberApps)
    # print "Average neg reviews:"+str(totalAvgNeg/numberApps)  
    # print "Average net reviews:"+str(totalAvgNet/numberApps)          

