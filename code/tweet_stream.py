#!/usr/bin/python3 

from kafka import KafkaProducer
from datetime import datetime

#import secret_config as conf ## where I put my Twitter API keys
import tweepy
import sys
import re
import time

TWEET_TOPICS = ['bitcoin','eth']

search_terms = ["$bitcoin", "$eth", "$doge"]

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'tweets'

class Streamer(tweepy.StreamingClient):

      # This function gets called when the stream is working
    def on_connect(self):

        print("Connected")

    def on_error(self, status_code):
        if status_code == 402:
            return False
            
            
      # This function gets called when a tweet passes the stream
    def on_tweet(self, tweet):

        # Displaying tweet in console
        if tweet.referenced_tweets == None:
            print(tweet.text)
            tweet = tweet.text

            tweet = re.sub(r'RT\s@\w*:\s', '', tweet)
            tweet = re.sub(r'https?.*', '', tweet)

            global producer
            producer.send(KAFKA_TOPIC, bytes(tweet, encoding='utf-8'))

            d = datetime.now()

            print(f'[{d.hour}:{d.minute}.{d.second}] sending tweet')
            # Delay between tweets
            time.sleep(0.5)
            
# Credentials (INSERT YOUR KEYS AND TOKENS IN THE STRINGS BELOW)
api_key = "="
api_secret = "="
bearer_token = r""
access_token = ""
access_token_secret = ""

# Gainaing access and connecting to Twitter API using Credentials
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

                          
stream = Streamer(bearer_token=bearer_token)

try:
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
except Exception as e:
    print(f'Error Connecting to Kafka --> {e}')
    sys.exit(1)
for term in TWEET_TOPICS:
    stream.add_rules(tweepy.StreamRule(term))
    
# Starting stream
stream.filter(tweet_fields=["referenced_tweets"])
    
