import time
import json

from singleton_decorator import singleton

from constants import Constants
from redis_conn import RedisConn


@singleton
class FraudChecks:

	def __init__(self):
		pass

	def check_fraud(self, data):
		if self.ip_fraud(data):
			return 'Fraud IP'
		if self.ad_stack(data):
			return 'Ad Stacked'
		return 'Clean Event'

	def ip_fraud(self, data):
		exists = RedisConn().bloom().cfExists(Constants.IP_CUCKOO_FILTER_NAME, data['ip'])
		self.publish(data, "Clean" if not exists else "Fraud")
		return exists

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
		RedisConn().redis().zadd(data.get('device_id'), {member: ts})
		count = RedisConn().redis().zcount(data.get('device_id'), ts - Constants.AD_STACK_WINDOW, ts)
		if count > Constants.AD_STACK_THRESHOLD:
			is_ad_stacked = True
		self.publish(data, "Fraud" if is_ad_stacked else "Clean")
		return is_ad_stacked

	def publish(self, data, status):
		data['status'] = status
		stream = Constants.CLEAN_STREAM_NAME if status == 'Clean' else Constants.FRAUD_STREAM_NAME
		RedisConn().redis().xadd(stream, data, id='*')
