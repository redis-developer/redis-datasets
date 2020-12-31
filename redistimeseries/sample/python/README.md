# An example Python client for Redis key-value store using RedisTimeSeries.

## Pre-requisite:

- Run RedisTimeSeries with Redis using redislabs/redismod container

```
docker run -d -p 6379:6379 redislabs/redismod
```

- Install python3

```
apt install python3
pip3 install redistimeseries
```

## Loading the timeseries data into Redis Server

Open loading.py script , change host and port of your Redis server

```
python3 loading.py 
```

```
python3 loading.py 
/root/python_timeseries_redis_client_example 
 /usr/lib/python38.zip 
 /usr/lib/python3.8 
 /usr/lib/python3.8/lib-dynload 
 /usr/lib/python3.8/site-packages

 Create new time series: temperature


 Append new value to time series:

 2020-12-31 05:50:16 : 38.61 
 2020-12-31 05:50:17 : 41.71 
 2020-12-31 05:50:18 : 23.17 
 2020-12-31 05:50:19 : 83.46 
 2020-12-31 05:50:20 : 68.26 
 2020-12-31 05:50:21 : 81.66 
 2020-12-31 05:50:22 : 53.03 
 2020-12-31 05:50:23 : 21.22 
 2020-12-31 05:50:24 : 10.07 
 2020-12-31 05:50:25 : 91.68 

 Query time series in range:

 2020-12-31 05:50:16 to 2020-12-31 05:50:25 

 2020-12-31 05:50:16 : 38.61 
 2020-12-31 05:50:17 : 41.71 
 2020-12-31 05:50:18 : 23.17 
 2020-12-31 05:50:19 : 83.46 
 2020-12-31 05:50:20 : 68.26 
 2020-12-31 05:50:21 : 81.66 
 2020-12-31 05:50:22 : 53.03 
 2020-12-31 05:50:23 : 21.22 
 2020-12-31 05:50:24 : 10.07 
 2020-12-31 05:50:25 : 91.68 


 Query time series in range:

 2020-12-31 05:50:20 to 2020-12-31 05:50:20 

 2020-12-31 05:50:20 : 68.26 


 Query time series info:
 ```
