
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
import time
from datetime import datetime

#DB info
client = MongoClient('localhost', 27017)
db=client.Apps 
###########################IMPORTANT: Change this field to the mongoDB collection you want##################
collection=db.matches

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
    
        
    #print newDictionary
    if newDictionary:
        newDictionary=json.loads(str(data))['results'][0]
        ios_starsVersionAllVersions_new="0.0"
        ios_price_new="0.0"
        ios_version_new="0.0"
        ios_ratingsAllVersions_new='0.0'

        if 'averageUserRating' in newDictionary:
            ios_starsVersionAllVersions_new= str((newDictionary['averageUserRating']))

        else:
            averageUserRating= "0.0" 


        if 'userRatingCount' in newDictionary:
            ios_ratingsAllVersions_new= str((newDictionary['userRatingCount']))

        else:
            averageUserRating= "0.0"       

        ios_price_new=str((newDictionary['price']))
        ios_version_new=str((newDictionary['version']))


        #print  '***********IOS***********'
        #print  'ios_averageUserRating:'+averageUserRating 
        #print  'ios_price_new:'+ios_price_new     
        #print  'ios_version_new:'+ios_version_new 

        return {'ios_starsVersionAllVersions_new':ios_starsVersionAllVersions_new,'ios_price_new':ios_price_new,'ios_version_new':ios_version_new,'ios_ratingsAllVersions_new':ios_ratingsAllVersions_new  }
    else:
        errorMSG= 'missing on ios'
        print errorMSG
        collection.find_one_and_update({"android_app_id":app_id_android}, {'$set': {'ios_missing':'true'}  })
        

#This method adds the missing fields to the android collection(*android_compatiblity & *android_ratingsAllCersions) 
def app_info(language='en_US'):
    count=0
    for post in collection.find().batch_size(30):
       if ('updated' not in post) and ('android_missing' not in post) and ('ios_missing' not in post): 
        time.sleep(2)
        #print str(datetime.now())
        count=count+1
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



        android_compatibility=''
        android_star_rating_new='0.0'
        android_version_string_new=''
        android_price='0.0'
        android_ratingsAllVersions ='0.0'


        android_ratingsAllVersions =data.find(class_="reviews-num")
        if android_ratingsAllVersions:
            android_ratingsAllVersions =data.find(class_="reviews-num").get_text()
        else:
            android_ratingsAllVersions ='0.0'

        android_compatibility=data.find(class_="title", text="Requires Android").parent
        if android_compatibility:
            android_compatibility=data.find(class_="title", text="Requires Android").parent.get_text()
        else:
            android_compatibility=''
        
        android_star_rating_new=data.find(class_="score")
        if android_star_rating_new:
            android_star_rating_new=data.find(class_="score").get_text()
        else:
            android_star_rating_new='0.0'    

        android_version_string_new=data.find(itemprop="softwareVersion")
        if android_version_string_new:
            android_version_string_new=data.find(itemprop="softwareVersion").get_text()
        else:
            android_version_string_new=''   


        android_price='0.0'
        
        if app_price is False:
            android_price=data.find(class_="price buy id-track-click")
            if android_price:
                try:
                    android_price=data.find(class_="price buy id-track-click").get_text().split("$")[1].split(" ")[0]
                except IndexError:
                    android_price='0.0'    
            
            else:
                android_price='0.0'    
       
        else:
            android_price='0.0'   


        print  'android_ratingsAllVersions:'+android_ratingsAllVersions 
        print  'android_compatibility:'+android_compatibility 
        print  'android_star_rating_new:'+android_star_rating_new 
        print  'android_version_string_new:'+android_version_string_new     
        print  'android price:'+android_price    
        #get iOS updated info
        app_id_ios=post['ios_url'].split("/id")[1].split("?")[0]
        #print app_id_ios
        try:
            ios_dicitionary=_app_info_ios(app_id_ios, app_id)
        except:
            continue    

        if ios_dicitionary:
            print  '***********IOS***********'
            print  'ios_starsVersionAllVersions_new:'+ios_dicitionary['ios_starsVersionAllVersions_new'] 
            print  'ios_price_new:'+ios_dicitionary['ios_price_new']    
            print  'ios_version_new:'+ios_dicitionary['ios_version_new'] 
            print  'ios_ratingsAllVersions_new:'+ios_dicitionary['ios_ratingsAllVersions_new'] 
            #print ios_starsVersionAllVersions_new_new
            print "######################################################"


            collection.find_one_and_update({"android_app_id":app_id}, {'$set': {'android_compatibility':android_compatibility
                                                                               ,'android_ratingsAllVersions':android_ratingsAllVersions
                                                                               ,'android_star_rating_new':android_star_rating_new
                                                                               ,'android_version_string_new':android_version_string_new
                                                                               ,'android_price':android_price
                                                                               ,'ios_starsVersionAllVersions_new':ios_dicitionary['ios_starsVersionAllVersions_new']
                                                                               ,'ios_price_new':ios_dicitionary['ios_price_new'] 
                                                                               ,'ios_version_new':ios_dicitionary['ios_version_new'] 
                                                                               ,'ios_ratingsAllVersions_new':ios_dicitionary['ios_ratingsAllVersions_new']
                                                                               ,'updated':True}  })
        else:
            continue
       
# Main method
if (__name__ == '__main__'):
     app_info()

