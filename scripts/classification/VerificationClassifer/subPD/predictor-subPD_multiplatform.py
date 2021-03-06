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
    totalMoney=0
    totalOther=0
    # the training data folder must be passed as first argument
    movie_reviews_data_folder = sys.argv[1]
    dataset = load_files(movie_reviews_data_folder, shuffle=False)

    for post in  collection_ios.find({'ios_numPD':{'$gte':1},'android_numPD':{'$gte':1}}).batch_size(30):
            count=count+1
            #print count
            numberApps=numberApps+1
            And_numberPosReviews=0
            And_numberNegReviews=0
            And_numberNeutReviews=0
            And_money=0
            And_other=0
            numberOfReviews=0
            #android_reviews=post['reviews']
            ios_reviews=post['ios_PDReviews']
            app_name=post['ios_name']
            android_app_id=post['android_app_id']
            # Predict the result on some short new sentences:
        #if app_name=="Vine":
            sentences = [
           
            ]

            for review in ios_reviews:
                sentences.append(review)
                #sentences.append(review['reviewBody'])
            #pickle.loads(saved_classifier)
            restored_classifier = joblib.load('subPDmodel_multiPlatform/mysentiment-classifier.pkl')


            predicted = restored_classifier.predict(sentences)

            for s, p in zip(sentences, predicted):
             if p==0:
                And_numberPosReviews=And_numberPosReviews+1
             elif p==1:
                And_numberNegReviews=And_numberNegReviews+1
             elif p==2:
                And_numberNeutReviews=And_numberNeutReviews+1 
             elif p==3:
                And_money=And_money+1 
             else:
                And_other=And_other+1
                        
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

            money=(float(And_money)/numberOfReviews)*100
            other=(float(And_other)/numberOfReviews)*100

            iosOtherClassifierStats={'critical':problemDiscovery,'appFeature':feautreRequest,'postUpdate':nonInformative,'moneyComplaints':money,'other':other}
            collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'iosSubPDClassifierStats':iosOtherClassifierStats}  })



            totalAvgPos=totalAvgPos+(float(And_numberPosReviews)/numberOfReviews)*100
            totalAvgNeg=totalAvgNeg+(float(And_numberNegReviews)/numberOfReviews)*100
            totalAvgNet=totalAvgNet+(float(And_numberNeutReviews)/numberOfReviews)*100
            #NEW
            totalMoney=totalMoney+(float(And_money)/numberOfReviews)*100
            totalOther=totalMoney+(float(And_other)/numberOfReviews)*100
            #print "****************************"


    print "Average Critical:"+str(totalAvgPos/numberApps)
    print "Average App feature:"+str(totalAvgNeg/numberApps)  
    print "Average post update:"+str(totalAvgNet/numberApps)
    #NEW
    print "Average money:"+str(totalMoney/numberApps)  
    print "Average Other:"+str(totalOther/numberApps)


def _getCollectionAndroid():

    And_numberPosReviews=0
    And_numberNegReviews=0
    And_numberNeutReviews=0
    And_money=0
    And_other=0
    numberApps=0
    totalAvgPos=0
    totalAvgNeg=0
    totalAvgNet=0
    totalMoney=0
    totalOther=0
    count=0
    # the training data folder must be passed as first argument
    movie_reviews_data_folder = sys.argv[1]
    dataset = load_files(movie_reviews_data_folder, shuffle=False)

    for post in  collection_ios.find({'ios_numPD':{'$gte':1},'android_numPD':{'$gte':1}}).batch_size(30):
            count=count+1
            #print count
            numberApps=numberApps+1
            And_numberPosReviews=0
            And_numberNegReviews=0
            And_numberNeutReviews=0
            And_money=0
            And_other=0
            numberOfReviews=0
            android_reviews=post['android_PDReviews']
            #ios_reviews=post['ios_reviews']
            app_name=post['ios_name']
            android_app_id=post['android_app_id']
            # Predict the result on some short new sentences:
        #if app_name=="Vine":
            sentences = [
           
            ]

            for review in android_reviews:
                #sentences.append(review['topic']+" "+review['review'])
                sentences.append(review)
            #pickle.loads(saved_classifier)
            restored_classifier = joblib.load('subPDmodel_multiPlatform/mysentiment-classifier.pkl')


            predicted = restored_classifier.predict(sentences)

            for s, p in zip(sentences, predicted):
             if p==0:
                And_numberPosReviews=And_numberPosReviews+1
             elif p==1:
                And_numberNegReviews=And_numberNegReviews+1
             elif p==2:
                And_numberNeutReviews=And_numberNeutReviews+1 
             elif p==3:
                And_money=And_money+1 
             else:
                And_other=And_other+1
                        
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

            money=(float(And_money)/numberOfReviews)*100
            other=(float(And_other)/numberOfReviews)*100

            iosOtherClassifierStats={'critical':problemDiscovery,'appFeature':feautreRequest,'postUpdate':nonInformative,'moneyComplaints':money,'other':other}
            collection_ios.find_one_and_update({"android_app_id":android_app_id}, {'$set': {'androidSubPDClassifierStats':iosOtherClassifierStats}  })



            totalAvgPos=totalAvgPos+(float(And_numberPosReviews)/numberOfReviews)*100
            totalAvgNeg=totalAvgNeg+(float(And_numberNegReviews)/numberOfReviews)*100
            totalAvgNet=totalAvgNet+(float(And_numberNeutReviews)/numberOfReviews)*100
            #NEW
            totalMoney=totalMoney+(float(And_money)/numberOfReviews)*100
            totalOther=totalMoney+(float(And_other)/numberOfReviews)*100
            #print "****************************"


    print "Average Critical:"+str(totalAvgPos/numberApps)
    print "Average App feature:"+str(totalAvgNeg/numberApps)  
    print "Average post update:"+str(totalAvgNet/numberApps)
    #NEW
    print "Average money:"+str(totalMoney/numberApps)  
    print "Average Other:"+str(totalOther/numberApps)

  

if __name__ == '__main__':
   print "ios stats:"
   _getCollectionIOS()
   print("********************") 
   print "android stats:"
   _getCollectionAndroid()             
          

