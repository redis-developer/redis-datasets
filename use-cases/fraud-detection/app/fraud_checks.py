import time
import os

from singleton_decorator import singleton

from constants import Constants
from redis_conn import RedisConn


@singleton
class FraudChecks:

	def __init__(self):
		self.click_spam_window_in_sec = int(os.getenv("CLICK_SPAM_WINDOW_IN_SEC", Constants.CLICK_SPAM_WINDOW_IN_SEC)) * 1000
		self.click_spam_threshold = int(os.getenv("CLICK_SPAM_THRESHOLD", Constants.CLICK_SPAM_THRESHOLD))

	def check_fraud(self, data):
		data['status'] = Constants.CLEAN
		data['fraud_type'] = Constants.CLEAN
		data['ts'] = int(time.time()*1000)
		if self.ip_fraud(data) or self.click_spam(data):
			pass
		self.publish(data)
		return data['fraud_type']

	def ip_fraud(self, data):
		exists = RedisConn().bloom().cfExists(Constants.IP_CUCKOO_FILTER_NAME, data['ip'])
		if exists:
			data['fraud_type'] = Constants.IP_BLACKLIST
			data['status'] = Constants.FRAUD

		return exists

	def click_spam(self, data):
		##
		# 'key' of each sorted is the device_id received.
		# click spam is True if the count in the range of scores (which is timestamp of event) -
		# - is greater than a threshold.
		#
		##
		is_click_spammed = False
		count = RedisConn().redis().zcount(data.get('device_id'), data['ts'] - self.click_spam_window_in_sec, data['ts'])
		if count >= self.click_spam_threshold:
			is_click_spammed = True
			data['fraud_type'] = Constants.CLICK_SPAM
			data['status'] = Constants.FRAUD
		return is_click_spammed

	def publish(self, data):
		RedisConn().redis().xadd(Constants.STREAM_NAME, data, id='*')
