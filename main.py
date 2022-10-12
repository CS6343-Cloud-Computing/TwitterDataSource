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


KafkaServer = os.environ.get('KafkaServer')
containerName = os.environ.get('ContainerName')

auth_kay_val = api_developer_authentication()
consumer_key = auth_kay_val.consumer_key_val()
consumer_secret = auth_kay_val.consumer_secret_val()
access_key = auth_kay_val.access_token_val()
access_secret = auth_kay_val.access_token_secret_val()
bearer_token = auth_kay_val.bearer_token_val()
producer = KafkaProducer(bootstrap_servers=[KafkaServer],api_version=(0,11,5))
MAX_CALL = 1
polling_interval = auth_kay_val.polling_time_interval()

consumer = KafkaConsumer(
 bootstrap_servers=KafkaServer, api_version=(0,11,5), auto_offset_reset='earliest', group_id=None
)
consumer.assign([TopicPartition(containerName, 0)])

client = tweepy.Client(bearer_token)
counter = 0
lastTweet = 0
query = '#Ukraine'
call_controller = 0


while True:
	hashs = DBConnect.getHashTags()
	print(hashs)
	for hash in hashs:
		query = hashs[hash]["query"]
		call_controller = 0
		lastTweet = 0
		headerSteps = hashs[hash]["steps"]
		pointer = hashs[hash]["pointer"] + 1
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
						print("=======> ", headerSteps[pointer])
						producer.send(headerSteps[pointer],  key = tweet_id.encode('utf-8'), value = str(tweet.text).encode('utf-8'),partition=0, headers=[('flow', "<-->".join(headerSteps).encode()), ('pointer', str(1).encode())])
						#break
			else:
				for tweet in tweepy.Paginator(client.search_recent_tweets,since_id = lastTweet, query=query, max_results = 10).flatten(limit = 200):
					if(counter == 0):
						lastTweet = tweet.id
						counter+=1
					else:
						tweet_id = str(tweet.id)
						print("=======> ", headerSteps[pointer])
						producer.send(headerSteps[pointer],  key = tweet_id.encode('utf-8'), value = str(tweet.text).encode('utf-8'),partition=0, headers=[('flow', "<-->".join(headerSteps).encode()), ('pointer', str(1).encode())])
						#break
			producer.flush()
	time.sleep(1)
			# time.sleep(polling_interval)
