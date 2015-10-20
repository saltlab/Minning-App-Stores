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
from bs4 import BeautifulSoup

appStores = {

'United States':      143441
}
#DB info
client = MongoClient('localhost', 27017)
db=client.Apps 
collection=db.iosAppsPilot

def getReviews(appStoreId, appId,maxReviews=-1):
    ''' returns list of reviews for given AppStore ID and application Id
        return list format: [{"topic": unicode string, "review": unicode string, "rank": int}]
    ''' 
    reviews=[]
    i=0
    while True: 
        ret = _getReviewsForPage(appStoreId, appId, i)
        if len(ret)==0: # funny do while emulation ;)
            break
        reviews += ret
        i += 1
        if maxReviews > 0 and len(reviews) > maxReviews:
            break
    return reviews

def _getReviewsForPage(appStoreId, appId, pageNo):
    userAgent = 'iTunes/9.2 (Macintosh; U; Mac OS X 10.6)'
    front = appStoreId
    url = "http://ax.phobos.apple.com.edgesuite.net/WebObjects/MZStore.woa/wa/viewContentsUserReviews?id=%s&pageNumber=%d&sortOrdering=4&onlyLatestVersion=true&type=Purple+Software" % (appId, pageNo)
    req = urllib2.Request(url, headers={"X-Apple-Store-Front": front,"User-Agent": userAgent})
    try:
        u = urllib2.urlopen(req, timeout=30)
    except urllib2.HTTPError:
        print "Can't connect to the AppStore, please try again later."
        raise SystemExit
    root = ElementTree.parse(u).getroot()
    reviews=[]
    for node in root.findall('{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}ScrollView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}View/{http://www.apple.com/itms/}MatrixView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/{http://www.apple.com/itms/}VBoxView/'):
        review = {}

        review_node = node.find("{http://www.apple.com/itms/}TextView/{http://www.apple.com/itms/}SetFontStyle")
        if review_node is None:
            review["review"] = None
        else:
            review["review"] = review_node.text

        version_node = node.find("{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}TextView/{http://www.apple.com/itms/}SetFontStyle/{http://www.apple.com/itms/}GotoURL")
        if version_node is None:
            review["version"] = None
        else:
            review["version"] = re.search("Version [^\n^\ ]+", version_node.tail).group()
    
        user_node = node.find("{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}TextView/{http://www.apple.com/itms/}SetFontStyle/{http://www.apple.com/itms/}GotoURL/{http://www.apple.com/itms/}b")
        if user_node is None:
            review["user"] = None
        else:
            review["user"] = user_node.text.strip()

        rank_node = node.find("{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}HBoxView")
        try:
            alt = rank_node.attrib['alt']
            st = int(alt.strip(' stars'))
            review["rank"] = st
        except KeyError:
            review["rank"] = None

        topic_node = node.find("{http://www.apple.com/itms/}HBoxView/{http://www.apple.com/itms/}TextView/{http://www.apple.com/itms/}SetFontStyle/{http://www.apple.com/itms/}b")
        if topic_node is None:
            review["topic"] = None
        else:
            review["topic"] = topic_node.text

        reviews.append(review)
    return reviews
    
def _print_reviews(reviews, country):
    ''' returns (reviews count, sum rank)
    '''
    if len(reviews)>0:
        print "Reviews in %s:" % (country)
        print ""
        sumRank = 0
        for review in reviews:
            print "%s by %s" % (review["version"], review["user"])
            for i in range(review["rank"]):
                sys.stdout.write ("*") # to avoid space or newline after print
            print " (%s) %s" % (review["topic"], review["review"])
            print ""
            sumRank += review["rank"]
        print "Number of reviews in %s: %d, avg rank: %.2f\n" % (country, len(reviews), 1.0*sumRank/len(reviews))
        return (len(reviews), sumRank)
    else:
        return (0, 0)

def _print_rawmode(reviews):
    for review in reviews:
         print json.dumps(review)
        
def _getCollection():
     apps=[]
     for post in collection.find():
         url=post['ios_url']
         apps.append(url)
         #print app_id
         
     
     return apps
     #return collection.find_one()

def _app_info(app_id, language='en_US'):
    print app_id
    url_play = 'https://itunes.apple.com/lookup?id=' 
    link = url_play + app_id
    request = urllib2.Request(link, headers={'Accept-Language': language})
    try:
        web = urllib2.urlopen(request).read()
        #print web
    except urllib2.HTTPError, e:
        return not_found(e)
    except urllib2.URLError, e:
        return not_found(e)
    except httplib.HTTPException, e:
        return not_found(e)
    except Exception:
        return not_found()

    data = BeautifulSoup(web)
    newDictionary=json.loads(str(data))
    return (newDictionary['results'][0]['description'])
    #print data.find(class_="product-review").get_text()
    #print data.find(class_="title", text="Requires Android").parent.get_text()     
def _add_reviews_description(url,reviews,description):
     data_string = json.dumps(reviews)
     print collection.find_one_and_update({"ios_url":url}, {'$set': {'ios_reviews':json.loads(data_string), 'ios_description':description}  })

def _add_reviews_test(url,reviews):
    for review in reviews:
         print type(review)  

if __name__ == '__main__':

   apps=_getCollection()

   for app in apps:

    app_id=app.split("id")[1].split("?")[0]
    reviews = getReviews(appStores['United States'], app_id,maxReviews=1)
    description=_app_info(app_id)
    _add_reviews_description(app,reviews,description)

