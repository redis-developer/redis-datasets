from redisbloom.client import Client
import time
import redis
from constants import Constants
from singleton_decorator import singleton
import json


@singleton
class FraudChecks:

	def __init__(self):

		self.redis_client = redis.Redis()
		self.bloom_client = Client()

	def check_fraud(self, data):
		if self.ip_fraud(data):
			return 'Fraud IP'
		if self.ad_stack(data):
			return 'Ad Stacked'
		return 'Clean'

	def ip_fraud(self, data):
		# Todo: initialize cf with data.
		return self.bloom_client.cfExists(Constants.IP_CUCKOO_FILTER_NAME, data['ip'])

	def ad_stack(self, data):
		##
		# 'key' of each sorted is the device_id received.
		# Ad stacked is True if the count in the range of scores (which is timestamp of event) -
		# - is greater than a threshold.
		#
		##
		ts = int(time.time() * 1000)
		is_ad_stacked = False
		member = json.dumps({'device_id': data['device_id'], 'transaction_id': data['transaction_id'], 'ts': ts})
		self.redis_client.zadd(data.get('device_id'), {member: ts})
		count = self.redis_client.zcount(data.get('device_id'), ts - Constants.AD_STACK_WINDOW, ts)
		if count > Constants.AD_STACK_THRESHOLD:
			is_ad_stacked = True
		return is_ad_stacked
