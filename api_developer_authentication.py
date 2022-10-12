import os
from dotenv import dotenv_values

class api_developer_authentication:

	def __init__(self):
		self.env_var = dotenv_values('.env')
		self.consumer_key = self.env_var['CLIENT_ID']
		self.consumer_secret = self.env_var['CLIENT_SECRET']
		self.access_token = self.env_var['ACCESS_TOKEN']
		self.access_token_secret = self.env_var['ACCESS_TOKEN_SECRET']
		self.bearer_token = self.env_var['BEARER_TOKEN']
		self.iteration = 2
		self.time_interval = 10 # value in second
		
	def consumer_key_val(self):
		return self.consumer_key
	def consumer_secret_val(self):
		return self.consumer_secret
	def access_token_val(self):
		return self.access_token
	def access_token_secret_val(self):
		return self.access_token_secret
	def bearer_token_val(self):
		return self.bearer_token
	def iteration_num(self):
		return self.iteration
	def polling_time_interval(self):
		return self.time_interval