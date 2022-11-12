from curses import meta
from requests import head
import tweepy
import time
import kafka
from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import TopicPartition
from api_developer_authentication import api_developer_authentication
import os
import DBConnect

KafkaServer = sys.argv[1]

auth_kay_val = api_developer_authentication()
consumer_key = auth_kay_val.consumer_key_val()
consumer_secret = auth_kay_val.consumer_secret_val()
access_key = auth_kay_val.access_token_val()
access_secret = auth_kay_val.access_token_secret_val()
bearer_token = auth_kay_val.bearer_token_val()
producer = KafkaProducer(bootstrap_servers=[KafkaServer],api_version=(0,11,5))
MAX_CALL = 1
polling_interval = auth_kay_val.polling_time_interval()

client = tweepy.Client(bearer_token)
counter = 0
lastTweet = 0
query = '#Ukraine'
call_controller = 0


while True:
	while(call_controller < MAX_CALL):
		counter = 0
		call_controller += 1
		if lastTweet == 0:
			for tweet in tweepy.Paginator(client.search_recent_tweets, query=query, max_results = 10).flatten(limit=200):
				print(tweet)
				if(counter == 0):
					lastTweet = tweet.id
					counter+=1
				else:
					tweet_id = str(tweet.id)
					producer.send("wfm-input",  key = tweet_id.encode('utf-8'), value = str(tweet.text).encode('utf-8'),partition=0, headers=[('workflow',int(sys.argv[2]).encode())])
		else:
			for tweet in tweepy.Paginator(client.search_recent_tweets,since_id = lastTweet, query=query, max_results = 10).flatten(limit = 200):
				if(counter == 0):
					lastTweet = tweet.id
					counter+=1
				else:
					tweet_id = str(tweet.id)
					producer.send("wfm-input",  key = tweet_id.encode('utf-8'), value = str(tweet.text).encode('utf-8'),partition=0, headers=[('workflow',int(sys.argv[2]).encode())])
		producer.flush()
	time.sleep(1)
			# time.sleep(polling_interval)
