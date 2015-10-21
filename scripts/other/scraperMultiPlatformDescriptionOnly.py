
from bs4 import BeautifulSoup

import json
import sys
import urllib
import urllib2
import pymongo
import jsonpickle
from pymongo import MongoClient

from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
from time import sleep
from datetime import datetime
import re
from random import randint

#DB info
client = MongoClient('localhost', 27017)
db=client.Apps 
###########################IMPORTANT: Change this field to the mongoDB collection you want##################
collection=db.matches2kNew

global webIos
global webAndroid
global newDictionary

def _getCollection():
     apps=[]
     for post in collection.find():
         appId=post['android_app_id']
         apps.append(appId)
         print appId
          
     return apps

def _app_info_ios(app_id,app_id_android, language='en_US'):
    #print app_id
    url_play = 'https://itunes.apple.com/lookup?id=' 
    link = url_play + app_id
    request = urllib2.Request(link, headers={'Accept-Language': language})
    try:
        webIos = urllib2.urlopen(request).read()
        data = BeautifulSoup(webIos, "html.parser")
        newDictionary=json.loads(str(data))['results']
        #print web
    except urllib2.HTTPError, e:
        #return not_found(e)
        errorMSG= 'missing on ios'
        print errorMSG
        collection.find_one_and_update({"android_app_id":app_id_android}, {'$set': {'ios_missing':'true'}  })
    except urllib2.URLError, e:
        return not_found(e)
    except httplib.HTTPException, e:
        return not_found(e)
    except Exception:
        return not_found()
    

    if newDictionary:
        newDictionary=json.loads(str(data))['results'][0]
        return {'ios_description':newDictionary['description']}
    else:
        errorMSG= 'missing on ios'
        print errorMSG
        collection.find_one_and_update({"android_app_id":app_id_android}, {'$set': {'ios_missing':'true'}  })
        

#This method adds the missing fields to the android collection(*android_compatiblity & *android_ratingsAllCersions) 
def app_info(language='en_US'):
    count=0
    timeCount=0
    for post in collection.find({'hasDescription':{'$exists':False}},no_cursor_timeout=True):
        count=count+1
        timeCount=timeCount+1
        if timeCount==10:
            timeCount=0
            sleep(randint(600,900))
        print "app count:"+str(count)
        app_id=post['android_app_id']
        app_price=post['android_free']
        app_id_ios=post['ios_url'].split("/id")[1].split("?")[0]

        print "app name:"+post['ios_name']
        print "app id:"+app_id

        url_play = 'https://play.google.com'
        link = url_play + '/store/apps/details?id=' + app_id
        request = urllib2.Request(link, headers={'Accept-Language': language})
        try:
            webAndroid = urllib2.urlopen(request).read()
            #print web
        except urllib2.HTTPError, e:
            #return not_found(e)
            print 'missing on Android'
            collection.find_one_and_update({"android_app_id":app_id}, {'$set': {'android_missing':'true'}  })
            try:
                _app_info_ios(app_id_ios,app_id)
            except:    
                continue
            continue    
        except urllib2.URLError, e:
            return not_found(e)
        except httplib.HTTPException, e:
            return not_found(e)
        except Exception:
            return not_found()

        data = BeautifulSoup(webAndroid, "html.parser")

        android_description=data.find(class_="id-app-orig-desc").get_text()

  
        #get iOS updated info
        app_id_ios=post['ios_url'].split("/id")[1].split("?")[0]
        #print app_id_ios
        try:
            ios_dicitionary=_app_info_ios(app_id_ios, app_id)
        except:
            print "EXCEPPPPPTTON"
            continue    

        if ios_dicitionary:
            collection.find_one_and_update({"android_app_id":app_id}, {'$set': {'android_description':android_description
                                                                               ,'ios_description':ios_dicitionary['ios_description']
                                                                               ,'hasDescription':True}  })
        else:
            continue
       
# Main method
if (__name__ == '__main__'):
     app_info()

