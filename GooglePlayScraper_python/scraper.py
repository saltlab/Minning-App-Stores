from bs4 import BeautifulSoup

import json
import sys
import urllib
import urllib2

# Max number of pages to click through when scraping reviews
MAX_PAGES_TO_SCRAPE = 100

# Google Play Reviews API base URL
# Give it a try:
# curl --data \
#   "reviewType=0&pageNum=15&id=com.inxile.BardTale&reviewSortOrder=2&xhr=1" \
#   https://play.google.com/store/getreviews
GOOGLE_PLAY_REVIEWS_URL = "https://play.google.com/store/getreviews"


class GooglePlayScrapedReview:
    '''
    Object returned from scraping Google Play reviews.
    '''

    def __init__(self, title, reviewText, delimiter='\n*********'):
        self.title = title.strip()
        self.reviewText = reviewText.strip()
        self.delimiter = delimiter

    def __str__(self):
        string = \
            ("%s%s%s%s" %
                (self.title,":\n", self.reviewText, self.delimiter))
        return string.encode('utf-8').strip()


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
        reviewBodyClass = "review-body"

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
    def generateScrapedObject(self, reviewBody):
        # Extract the review title
        reviewTitleClass = "review-title"
        reviewTitle = reviewBody.find(class_=reviewTitleClass).get_text()

        # Extract the review body
        reviewBodyContentIdx = 2
        reviewBody = reviewBody.contents[reviewBodyContentIdx]

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


# Main method
# Play around to get a feel for this
if (__name__ == '__main__'):
    PACKAGE_NAME = "com.hottrix.ibeerfree"
    NUM_PAGES_TO_SCRAPE = 100

    gs = GooglePlayReviewScraper(PACKAGE_NAME)
    scraped = gs.scrape(pageNumbers=100)

    for review in scraped:
        print(review)
