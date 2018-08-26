## SAMPLE CODE TO PREDICT WHETHER STOCK PRICES WILL GO UP OR DOWN BASED ON SENTIMENT ANALYSIS

### This is an example of how I'd approach a model to forecast whether stock prices of the Mexican airline "Volaris" will go up or down depending on the number of positive, negative and neutral tweets from the previous day. This example is done using Cloudera VM 5.8 and Python 3.

##General steps:

Extraction of data: The first step is the extraction of tweets. At the beginning I perfomed the extraction using Apache Flume and the API provided by twitter and I managed to store the tweets in HDFS, however the data was corrupted due to Spanish characters which do not exist in English. So I performed a second extraction of tweets using the library Tweepy in Python which I found more convenient because it allowed me to extract tweets by hashtag and bound by date. For stock prices, I downloaded the data manually from Investing.com, however this can be done using web scrapping in Python as well.

Data cleaning: Using the method regex_replace`dd`









