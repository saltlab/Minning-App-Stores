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
import re
import stem
import stem.connection

import time
import urllib2

from stem import Signal
from stem.control import Controller

# initialize some HTTP headers
# for later usage in URL requests
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}
# initialize some
# holding variables
oldIP = "0.0.0.0"
newIP = "0.0.0.0"

# how many IP addresses
# through which to iterate?
nbrOfIpAddresses = 3

# seconds between
# IP address checks
secondsBetweenChecks = 2

# Max number of pages to click through when scraping reviews
MAX_PAGES_TO_SCRAPE = 100

# Google Play Reviews API base URL
# Give it a try:
# curl --data \
#   "reviewType=0&pageNum=15&id=com.inxile.BardTale&reviewSortOrder=2&xhr=1" \
#   https://play.google.com/store/getreviews
GOOGLE_PLAY_REVIEWS_URL = "https://play.google.com/store/getreviews"

#DB info
client = MongoClient('localhost', 27017)
db=client.Apps 
collection=db.matches1k



class GooglePlayScrapedReview:
    '''
    Object returned from scraping Google Play reviews.
    '''

    def __init__(self, title, reviewText,date,author,rank):
        self.title = title.strip()
        self.reviewText = reviewText.strip()
        self.date=date.strip()
        self.author=author.strip()
        self.rank=rank.strip()
  


    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)    


class GooglePlayReviewScraperException(Exception):
    pass


class GooglePlayReviewScraper:
    '''
    Essentially, fires off a number of POST requests to the Google Play
    to simulate client requests.

    These requests (as of Sept 8, 2013) are in the format:

      reviewType:0            [???]
      pageNum:11              [pagination]
      id:com.inxile.BardTale  [package name]
      reviewSortOrder:2       [???]
      xhr:1                   [???]

    [???] means I don't know what the param is for.

    '''

    def __init__(self, packageName, maxNumberOfPages=MAX_PAGES_TO_SCRAPE):
        self.packageName = packageName
        self.maxNumberOfPages = maxNumberOfPages
        self.postParams = \
            {
                'reviewType': 0,
                'pageNum': 0,
                'id': packageName,
                'reviewSortOrder': 2,
                'xhr': 1
            }

    def scrapePageNumber(self, pageNum=0):
        # Modify POST params to use required pageNum param
        pagedPostParams = self.postParams.copy()
        pagedPostParams['pageNum'] = pageNum

        # Encode
        encodedPostParams = urllib.urlencode(pagedPostParams)

        # Fire dat POST
        #return urllib2.urlopen(GOOGLE_PLAY_REVIEWS_URL, encodedPostParams).read()
        return requestReviews(GOOGLE_PLAY_REVIEWS_URL,encodedPostParams)

    def parseResult(self, postResults):
        # Magic indices required for parsing Google API results
        contentIdx = 0
        apiJsonStartIndex = 6
        htmlStartIndex = 2

        # Classes for parsing
        reviewBodyClass = "single-review"

        # Read in the API Request
        postResultsString = postResults

        # Attempt to parse result
        try:
            result = \
                json.loads(
                    postResultsString[apiJsonStartIndex:]
                )[contentIdx][htmlStartIndex]
            htmlResult = BeautifulSoup(result, "html.parser")

            parsedResults = \
                [self.generateScrapedObject(reviewBody) for
                    reviewBody in htmlResult.find_all(class_=reviewBodyClass)]

            #print parsedResults
            return parsedResults

        except:
            raise \
                GooglePlayReviewScraperException(
                    "Exception: %s. Bad parse: %s" %
                    (sys.exc_info()[0], postResults)
                )

    @classmethod
    def generateScrapedObject(self, review):
        # Extract the review title
        reviewTitleClass = "review-title"
        reviewTitle = review.find(class_=reviewTitleClass).get_text()

        # Extract the review body
        reviewBodyClass = "review-body"
        reviewBody = review.find(class_=reviewBodyClass).get_text()

        # Extract the review date
        reviewDateClass = "review-date"
        reviewDate = review.find(class_=reviewDateClass).get_text()

        # Extract the review author
        reviewAuthorClass = "author-name"
        reviewAuthor = review.find(class_=reviewAuthorClass).get_text()

        # Extract the review rank
        reviewRankClass = "review-info-star-rating"
        #reviewRank = review.find(class_=reviewRankClass).get_text()
        reviewRank = review.find("div", attrs={"class": "tiny-star star-rating-non-editable-container"})["aria-label"]
        #print int(reviewRank.split()[0])
        #print reviewRank
        #print (type(reviewRank)
        reviewRank= reviewRank.split("Rated ")[1].split(" stars")[0]


        #print get_num(reviewRank)
        s = reviewTitle.encode('utf8')
        search=re.escape(s)
        reviewBodyFixed= reviewBody.split("Full Review")[0]

        return {'reviewBody':reviewBodyFixed}
    def scrape(self, pageNumbers=None):
        parsedResults = []
        scrapePageNums = pageNumbers or self.maxNumberOfPages

        try:
            for pageNum in xrange(scrapePageNums):
                results = self.parseResult(self.scrapePageNumber(pageNum))
                time.sleep(3)
                for result in results:
                    parsedResults.append(result)
        except GooglePlayReviewScraperException as e:
            print("Bad Parse: %s" % e)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        finally:
            return parsedResults


     #return collection.find_one()
def _add_reviews(appId,reviews):
     data_string = json.dumps(reviews)
     collection.find_one_and_update({"android_app_id":appId}, {'$set': {'reviews':json.loads(data_string) ,'updated_reviews_android':True}  })

# request a URL 
def request(url):
    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    # request a URL
    # via the proxy
    _set_urlproxy()
    request=urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()
# request a URL 
def requestReviews(url,params):
    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    # request a URL
    # via the proxy
    _set_urlproxy()
    request=urllib2.Request(url, params, headers)
    return urllib2.urlopen(request).read()


# signal TOR for a new connection 
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'klaiee321')
        controller.signal(Signal.NEWNYM)
        controller.close()

# Main method
# Play around to get a feel for this
if (__name__ == '__main__'):
    for app in collection.find({'updated_reviews_android':{'$exists':False}}).batch_size(30):
        print 'hello'
        if oldIP == "0.0.0.0":
            renew_connection()
            oldIP = request("http://icanhazip.com/")
        else:
            oldIP = request("http://icanhazip.com/")
            renew_connection()
            newIP = request("http://icanhazip.com/")
        while oldIP == newIP:
            newIP = request("http://icanhazip.com/")
            print request("http://icanhazip.com/")
            
            appId=app['android_app_id'] 
            print appId   
            try:
                 gs = GooglePlayReviewScraper(appId)
                 scraped = gs.scrape(pageNumbers=25)
                 _add_reviews(appId,scraped)
            except:
                continue
            time.sleep(randint(8,12))         
