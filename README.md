## SAMPLE CODE TO PREDICT WHETHER STOCK PRICES WILL GO UP OR DOWN BASED ON SENTIMENT ANALYSIS

### This is an example of how I approached a model to forecast whether stock prices of the Mexican airline "Volaris" will go up or down depending on the number of positive, negative and neutral tweets from the previous day. This example is done using Cloudera VM 5.8 and Python 3.

### General steps:

### Extraction of data 

The first step is the extraction of tweets. At the beginning I perfomed the extraction using Apache Flume and the API provided by twitter and I managed to store the tweets into HDFS, however the data was corrupted due to Spanish characters which do not exist in English. To solve this issue, I performed a second extraction of tweets using the library Tweepy in Python which I found more convenient because it allowed me to extract tweets by hashtag (e.g. `#volaris`) and bound by date. For stock prices, I downloaded the data manually from Investing.com, however this can be done using web scrapping in Python as well.

### Data cleaning

Using mostly the method `regexp_replace` together with a couple of regex expressions, I replaced those Spanish characters by English characters (e.g. `aerolínea` is replaced by `aerolinea`). Also I removed hashtags, replace URL's by the word `url` and users by the word `user`.

In the same script I used the method `Tokenizer` which will transform a tweet into a vector of strings, and then the method `StopWordsRemover` which will remove irrelevant words for the sentiment analysis.

### Bulding a sentiment classification model

In the next script, I applied the method `Word2Vec` to transform the output of `StopWordsRemover` into numeric vectors. I classified manually the corresponding tweets into positive (0), negative (1) or neutral (2) which I attached to the dataframe of numeric vectors. Using `randomSplit` to split my data into training-testing (70%-30%), I fit a `RandomForestClassifier` on the training data and using `MulticlassClassificationEvaluator` I measure its performance on the testing dataset.

### Getting count of positive, negative and neutral tweets per day.

After getting predictions from the previous sentiment classification model, I perform a `groupBy().count()` in order to count how the how many positive, negative and neutral tweets are per day. I write the output count into a CSV file.

### Building the main dataframe

A single python script is devoted to construct the main dataframe. This dataframe has 3 feature variables, namely the number of positive tweets per day, the number of negative tweets per day and the number of neutral tweets per day. This dataframe contains as many rows as available days. These feature variables come from the previous CSV file. The target variable consists of two classes, 1 if the stock price went up the next day and 0 otherwise. This is constructed by reading a CSV file containing the closing stocking prices of Volaris downloaded from Investing.com, applying some transformation to convert those prices into 0's and 1's based on the required condition, and finally filling up Saturday and Sunday by defining the price for Saturday as the average of the prices corresponding to Friday and Monday, and defining the price of Sunday as the average of the prices for Saturday and Monday. The resulting dataframe is written as CSV file.

### Applying logistic regression on the main dataframe

Finally, using `randomSplit`, `VectorAssembler`, `StringIndexer`, `MulticlassClassificationEvaluator` and `LogisticRegression`, I train a logistic regression on the training data and measure the accuracy on the testing data.












