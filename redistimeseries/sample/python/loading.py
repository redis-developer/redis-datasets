# An example Python client for Redis key-value store using RedisTimeSeries.
from redistimeseries.client import Client as RedisTimeSeries
import time
import sys
import site
import datetime
import random

print(' \n '.join(sys.path))

ts = RedisTimeSeries(host='localhost', port=6379)

#ts.flushdb()

key = 'temperature'

def create(key):

	print('\n Create new time series: %s' % str(key))

	#ts.create(key,retentionSecs=30,labels={'sensor_id' : 2,'area_id' : 32})
	ts.create(key,retention_msecs=30000,labels={'sensor_id' : 2,'area_id' : 32})

	print('')

def store(key, interval):

	print("\n Append new value to time series:\n")

	begin_time = int(time.time())

	for i in range(interval):

		timestamp = int(time.time())

		value = round(random.uniform(0.0,100.0),2)

		timestamp_strftime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

		sys.stdout.write(' %s : %.2f \n' % (timestamp_strftime, value))

		sys.stdout.flush()

		#ts.add(key,timestamp,value,retentionSecs=30, labels={'sensor_id' : 2,'area_id' : 32})
		ts.add(key,timestamp,value,retention_msecs=30000, labels={'sensor_id' : 2,'area_id' : 32})

		time.sleep(1)

	end_time = int(time.time()-1)

	return (begin_time, end_time)

def query(key, begin_time, end_time):

	begin_time_datetime = datetime.datetime.fromtimestamp(begin_time).strftime('%Y-%m-%d %H:%M:%S')

	end_time_datetime = datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

	print("\n Query time series in range:\n\n %s to %s \n" % (begin_time_datetime, end_time_datetime))

	try:
		#for record in ts.range(key,begin_time, end_time,bucketSizeSeconds=1):
		for record in ts.range(key,begin_time, end_time,bucket_size_msec=1000):

			timestamp = datetime.datetime.fromtimestamp(record[0]).strftime('%Y-%m-%d %H:%M:%S')
			
			value = round(float(record[1]),2)

			print(' %s : %.2f ' % (timestamp,value))

	except Exception as e:
		print("\n Error: %s" % e)

	print('')

def print_info():

	print('\n Query time series info:\n')

	for key in ts.keys('*'):
		print(' key=%s' % (key.decode('utf8')))
		info = ts.info(key)
		sensor = info.labels['sensor_id']
		print(" sensor_id=%s " % str(sensor))
		area = info.labels['area_id']
		print(" area_id=%s " % str(area))
		last_time_stamp_seconds = info.__dict__['lastTimeStamp']
		last_time_stamp = datetime.datetime.fromtimestamp(last_time_stamp_seconds).strftime('%Y-%m-%d %H:%M:%S')
		print(" last_time_stamp=%s " % str(last_time_stamp))

	print('')

def print_loop(loops):

	for i in range(loops):

		if i == 0:
			sys.stdout.write(' ')

		sys.stdout.write('.')
		sys.stdout.flush()
		time.sleep(1)

	print('')

create(key)

interval = 10

begin_time, end_time = store(key,interval)

time.sleep(1)

query(key,begin_time,end_time)

query(key,begin_time+4,end_time-5)

print_info()

print('\n Set expire key: %s' % str(key))

ts.expire(key, (30))

loops = 30

print_loop(loops)

query(key,begin_time,end_time)

time.sleep(1)

interval = 1

create(key)

begin_time, end_time = store(key,interval)

time.sleep(1)

query(key,begin_time,end_time)

time.sleep(1)

print('\n Delete key: %s' % str(key))

ts.delete(key)

time.sleep(1)

query(key,begin_time,end_time)

print('')
