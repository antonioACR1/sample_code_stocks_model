import tweepy
import csv
import pandas as pd

consumer_key = 'ScvEvhT6tUK7kiVuD3HohF82A'
consumer_secret = 'ILu2l3M7ybq6bfGono0C4xOyh9KOelpCqFxbrEwIwiF7JlPk7V'
access_token = '877848902-yzXJ9nMkrt6iDPIuc62s4Pum2KTSIbDKnHqExZPE'
access_token_secret = '3cxI5ZXotgR72nS5cB3rwSC9P3tbWcbiLZjpQz5CiYcJb'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

csvFile = open('vol.csv', 'a')
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q="#volaris",count=1000,
                           since="2018-01-01").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
	
df=pd.read_csv("C:/Users/USUARIO/Documents/vol.csv",header=None,names=["fecha","tweet"])

df.to_csv("tweetsVolaris.csv",index=False)
