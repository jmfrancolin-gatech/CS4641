import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import signal
import time
import sys
import os

consumer_key = XXX
consumer_secret = XXX
access_token = XXX
access_token_secret = XXX

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#print(api.me().name)

# get all tweets and put them in python list
def get_tweets(username, affiliation, data_type):
        # query meta data
        tweets_meta_data = api.user_timeline(screen_name = username, count = 200, tweet_mode='extended')
        tweets_list = [tweet.full_text.encode('utf-8').strip() + ' ' for tweet in tweets_meta_data]
        file_name = username + "." + affiliation + ".txt"

        if (data_type == "train"):
            path = "../train-tweets"
            with open(os.path.join(path, file_name), 'w') as file:
                for tweet in tweets_list:
                    file.write(tweet)
                file.close()

        elif (data_type == "test"):
            path = "../test-tweets"
            with open(os.path.join(path, file_name), 'w') as file:
                for tweet in tweets_list:
                    file.write(tweet)
                file.close()

if (len(sys.argv) == 4 and (sys.argv[2] == "dem" or sys.argv[2] == "rep")):
    username = sys.argv[1][1:]
    affiliation = sys.argv[2]
    data_type = sys.argv[3]
else:
    print("Usage: python twitter_listener.py @username dem/rep train/test")
    sys.exit(0)


item = api.get_user(username)
print("name: " + item.name)
print("affiliation: " + affiliation)
get_tweets(username, affiliation, data_type)