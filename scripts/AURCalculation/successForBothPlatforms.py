from pymongo import MongoClient
import csv
import stats


#From DB
client_ios = MongoClient('localhost', 27017)
db_ios = client_ios.Apps
collection_ios = db_ios.appPairs80k


android_ratings_average = 0
android_stars_average = 0

ios_ratings_average = 0
ios_stars_average = 0


def _getRatingStarsAverages():
    android_ratings = []
    ios_ratings = []
    android_stars = []
    ios_stars = []

    global android_ratings_average
    global android_stars_average

    global ios_ratings_average
    global ios_stars_average

    print collection_ios.count({'android_ratings_float': {'$gte': 1}, 'ios_ratings_float':{'$gte': 1}}, no_cursor_timeout=True)
    for app in collection_ios.find({'android_ratings_float': {'$gte': 1}, 'ios_ratings_float':{'$gte': 1}}, no_cursor_timeout=True):
        android_ratings.append(app['android_ratings_float'])
        android_stars.append(app['android_stars_float'])
        #ios stats
        ios_ratings.append(app['ios_ratings_float'])
        ios_stars.append(app['ios_stars_float'])

    android_ratings_average = stats.mean(android_ratings)
    android_stars_average = stats.mean(android_stars)

    ios_ratings_average = stats.mean(ios_ratings)
    ios_stars_average = stats.mean(ios_stars)

    print "android"
    print android_ratings_average
    print android_stars_average

    print "ios"
    print ios_ratings_average
    print ios_stars_average


def _getCollection():
    print "Sanity Check"
    print "android"
    print android_ratings_average
    print android_stars_average

    print "ios"
    print ios_ratings_average
    print ios_stars_average

    ratings_combined_average = stats.mean([android_ratings_average, ios_ratings_average])
    stars_combined_average = stats.mean([android_stars_average, ios_stars_average])

    print "average:"
    print ratings_combined_average
    print stars_combined_average
    for post in collection_ios.find({'android_ratings_float': {'$gte': 1}, 'ios_ratings_float':{'$gte': 1}}, no_cursor_timeout=True):
        android_app_id = post['android_app_id']
        android_app_rating = post['android_ratings_float']
        android_app_star = post['android_stars_float']

        ios_app_rating = post['ios_ratings_float']
        ios_app_star = post['ios_stars_float']

        successAndroid = (float(_sucess(android_app_rating, android_app_star, ratings_combined_average, stars_combined_average)) / 5) * 100
        successIos = (float(_sucess(ios_app_rating, ios_app_star, ratings_combined_average, stars_combined_average)) / 5) * 100

        collection_ios.find_one_and_update({"android_app_id": android_app_id}, {'$set': {'android_success_average': successAndroid, 'ios_success_average': successIos}})


def outputCsv():
    apps = []
    csvfile = "iosVsAndroid.csv"
    for post in  collection_ios.find({'ios_success_average':{'$exists':True}, 'android_success_average':{'$exists':True}}, no_cursor_timeout=True):
        apps.append({"id": post['android_app_id'], "ios_success_average": post['ios_success_average'], "android_success_average": post['android_success_average']}) 
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(["id","ios_success_average", "android_success_average", "difference"])
        for app in apps:
            title=app['id']
            writer.writerow([title.encode('utf-8').strip(),app['ios_success_average'], app['android_success_average'], float(app['android_success_average']) - app['ios_success_average'] ])


def _sucess(app_rating, app_star, ratings_average, stars_average):
    return float((float(app_rating) * app_star) + (float(ratings_average) * stars_average)) / float(app_rating + ratings_average)
if __name__ == '__main__':
    _getRatingStarsAverages()
    _getCollection()
    #outputCsv()
