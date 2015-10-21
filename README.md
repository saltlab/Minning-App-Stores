# Minning iOS and Android App-pairs

A Large Scale Empirical Study on iOS and Android Mobile App-pairs. The repo is split into 
two directories, where the "Data" directory contains a set of 80,169 app-pairs along with their attributes such as price, rating, stars etc..
The Data directory contains a txt file which has a dropbox link to a set of 2003 app-pairs along with their user reviews (We couldn't upload
that dataset here due to github's file size restrictions). Both of these datasets are JSON objects and can be imported directly to any mongoDB instance by using the following command:
"mongoimport --db inserDBNameHere --collection insertCollectionNameHere --file insertDataSetNameHere"

The other directory "scripts" contains all the scripts we used to generate the data and proccess it.

We hope that by open sourcing our work we encourage others to conduct more research on mobile app-pairs.

If you have any questions or comments please don't hesitate to contact me at mohamed.ali92ubc@gmail.com

Thanks!
