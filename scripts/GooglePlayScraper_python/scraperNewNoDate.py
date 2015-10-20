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
collection=db.iosAppsPilot



class GooglePlayScrapedReview:
    '''
    Object returned from scraping Google Play reviews.
    '''

    def __init__(self, title, reviewText):
        self.title = title.strip()
        self.reviewText = reviewText.strip()

  


    
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
        return urllib2.urlopen(
            GOOGLE_PLAY_REVIEWS_URL, encodedPostParams).read()

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
            htmlResult = BeautifulSoup(result)

            parsedResults = \
                [self.generateScrapedObject(reviewBody) for
                    reviewBody in htmlResult.find_all(class_=reviewBodyClass)]

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
        return GooglePlayScrapedReview(reviewTitle, reviewBody)

    def scrape(self, pageNumbers=None):
        parsedResults = []
        scrapePageNums = pageNumbers or self.maxNumberOfPages

        try:
            for pageNum in xrange(scrapePageNums):
                results = self.parseResult(self.scrapePageNumber(pageNum))
                for result in results:
                    parsedResults.append(result)
        except GooglePlayReviewScraperException as e:
            print("Bad Parse: %s" % e)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        finally:
            return parsedResults


def _getCollection():
     apps=[]
     for post in collection.find():
         appId=post['android_app_id']
         apps.append(appId)
         print appId
         
     
     return apps
     #return collection.find_one()
def _add_reviews(appId,reviews):
     #reviewsNew =list(reviews)
     reviewsJson=[]

     for review in reviews:
        #print jsonpickle.encode(review)
        reviewsJson.append( json.dumps(review.__dict__))

     
     #print (reviewsJson.to_JSON())
     #print json.loads(json.dumps(reviewsJson))
     temp= jsonpickle.encode(reviewsJson)
     data_string = json.dumps(reviewsJson)
     collection.find_one_and_update({"android_app_id":appId}, {'$set': {'android_reviews':jsonpickle.decode(temp)}  })

def app_info(app_id, language='en_US'):
    print app_id
    url_play = 'https://play.google.com'
    link = url_play + '/store/apps/details?id=' + app_id
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

    android_reviews_sum =data.find(class_="reviews-num").get_text()
    android_compatibility=data.find(class_="title", text="Requires Android").parent.get_text()
    android_description=data.find(class_="id-app-orig-desc").get_text()
    print android_description
    collection.find_one_and_update({"android_app_id":app_id}, {'$set': {'android_compatibility':android_compatibility, 'android_ratingsAllVersions':android_reviews_sum,'android_description':android_description}  })
# Main method
# Play around to get a feel for this
if (__name__ == '__main__'):
    PACKAGE_NAME = "com.hottrix.ibeerfree"
    NUM_PAGES_TO_SCRAPE = 100

    apps=_getCollection()
    for app in apps:

     gs = GooglePlayReviewScraper(app)
     scraped = gs.scrape(pageNumbers=1)
     _add_reviews(app,scraped)
     app_info(app)

