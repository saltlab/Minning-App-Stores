
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
from random import randint
from time import sleep


#DB info
client = MongoClient('localhost', 27017)
db=client.Apps 
collection=db.matches80k

def _app_info_android(app_id,language='en_US'):
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
        return None   
    except urllib2.URLError, e:
        return None
    except httplib.HTTPException, e:
        return None
    except Exception:
        return None

    data = BeautifulSoup(webAndroid, "html.parser")

    android_last_updated=data.find(class_="title", text="Updated").parent
    if android_last_updated:
        android_last_updated=data.find(class_="title", text="Updated").parent.get_text().split(' Updated ')[1]
        #android_description=data.find(class_="id-app-orig-desc").get_text()
        lastUpdatedFinal= (datetime.datetime.strptime(android_last_updated, "%d %B %Y ").strftime("%Y-%m-%d"))
        #print "android:"+lastUpdatedFinal
        return lastUpdatedFinal
    else:
        return None





def _app_info(language='en_US'):
 count=0
 pauseCounter = 0
 for post in collection.find({'update_dates':{'$exists':False}},no_cursor_timeout=True):

    if pauseCounter==600:
        pauseCounter=0
        sleep(randint(180,300))
    count=count+1
    pauseCounter=pauseCounter+1
    app_name=post['ios_name']
    app_url=post['ios_url']
    app_id_android=post['android_app_id']
    app_id=app_url.split("id")[1].split("?")[0]
    request2 = urllib2.Request(app_url, headers={'Accept-Language': language})
    try:
        web = urllib2.urlopen(request2).read()
    except urllib2.HTTPError, e:
        continue
    except urllib2.URLError, e:
        continue
    except httplib.HTTPException, e:
        continue
    except Exception:
        continue


    data2 = BeautifulSoup(web, "html.parser")
    lastUpdated=data2.find(class_="release-date")
    if lastUpdated:
        lastUpdated=data2.find(class_="release-date").get_text().split(": ")[1]
        lastUpdatedStripped=lastUpdated.replace(',','')
        
        lastUpdatedFinal= (datetime.datetime.strptime(lastUpdatedStripped, "%b %d %Y").strftime("%Y-%m-%d"))
        #print 'name:'+app_name
        #print 'ios:'+ lastUpdatedFinal
        lastUpdatedFinalDT=datetime.datetime.strptime(lastUpdatedFinal, "%Y-%m-%d")
        #print 'last updated Format:'+ lastUpdatedFinalDT
        #releaseDateDT=datetime.datetime.strptime(releaseDate, "%Y-%m-%d")
        #difference= (abs((lastUpdatedFinalDT - releaseDateDT).days))
        #differenceYears=difference / (365.25)

        #Get Android Date
        lastUpdatedAndroidFinal=_app_info_android(app_id_android)

        if lastUpdatedAndroidFinal:
            lastUpdatedAndroidFinalDT=datetime.datetime.strptime(lastUpdatedAndroidFinal, "%Y-%m-%d")
            #Android - iOS
            difference= (abs((lastUpdatedAndroidFinalDT - lastUpdatedFinalDT).days))
            differenceYears=difference / (365.25)
            #print "difference in days:"+str(difference)
            dates={'ios_update_date':lastUpdatedFinalDT,'android_updated_date':lastUpdatedAndroidFinalDT,'differenceDays':difference,'differenceYears':differenceYears}
            collection.find_one_and_update({"ios_url":app_url}, {'$set': {'update_dates':dates}  })
            #print "success"
            print "# of apps processed:"+str(count)


        else:
            continue
    else:
        continue


if __name__ == '__main__':

    _app_info()


