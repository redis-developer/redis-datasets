# Timeseries in Redis with RedisTimeSeries

## What is a Timeseries Dataset


Time Series data is sequential data. Analysis of this data is often reduced to running aggregration queries to reduce processing overhead and to extract intelligence in real time. We can use RedisTimeseries to help us achieve this.

## Use Cases

- Stock ticker data
- IoT sensor data
- Fleet management (vehicle id, timestamp, GPS coordinates, average speed)
- Requiring a database where other RDBMS are too heavy


## Pre-requisite

- Run Redis Server with RedisTimeSeries Modules enabled

```
docker run -d -p 6379:6379 redislabs/redismod
```

- Install Python3

```
brew install python3
```

## Demo


```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redistimeseries/sample/sensor_data/
```


Within the scripts folder run:

```
 python3 populate_timeseries.py --host localhost --port 6379 --sensor-id=10
```

Then exec into Redis:

```
 redis-cli
127.0.0.1:6379> keys *
1) "humidity:10"
2) "temperature:10"
127.0.0.1:6379> 
```

```
2 [0 172.17.0.1:55428] "TS.ADD" "temperature:10" "*" "14" "LABELS" "__name__" "temperature" "sensor" "10"
1609222124.630468 [0 172.17.0.1:55428] "TS.ADD" "humidity:10" "*" "79" "LABELS" "__name__" "humidity" "sensor" "10"
1609222125.635493 [0 172.17.0.1:55428] "TS.ADD" "temperature:10" "*" "10" "LABELS" "__name__" "temperature" "sensor" "10"
1609222125.636849 [0 172.17.0.1:55428] "TS.ADD" "humidity:10" "*" "71" "LABELS" "__name__" "humidity" "sensor" "10"
1609222126.639874 [0 172.17.0.1:55428] "TS.ADD" "temperature:10" "*" "16" "LABELS" "__name__" "temperature" "sensor" "10"
1609222126.641306 [0 172.17.0.1:55428] "TS.ADD" "humidity:10" "*" "78" "LABELS" "__name__" "humidity" "sensor" "10"
1609222127.647946 [0 172.17.0.1:55428] "TS.ADD" "temperature:10" "*" "13" "LABELS" "__name__" "temperature" "sensor" "10"
1609222127.649274 [0 172.17.0.1:55428] "TS.ADD" "humidity:10" "*" "73" "LABELS" "__name__" "humidity" "sensor" "10"
1609222128.653979 [0 172.17.0.1:55428] "TS.ADD" "temperature:10" "*" "16" "LABELS" "__name__" "temperature" "sensor" "10"
1609222128.655296 [0 172.17.0.1:55428] "TS.ADD" "humidity:10" "*" "74" "LABELS" "__name__" "humidity" "sensor" "10"
1609222129.657474 [0 172.17.0.1:55428] "TS.ADD" "temperature:10" "*" "11" "LABELS" "__name__" "temperature" "sensor" "10"
1609222129.658831 [0 172.17.0.1:55428] "TS.ADD" "humidity:10" "*" "77" "LABELS" "__name__" "humidity" "sensor" "10"
1609222130.662568 [0 172.17.0.1:55428] "TS.ADD" "temperature:10" "*" "13" "LABELS" "__name__" "temperature" "sensor" "10"
1609222130.664954 [0 172.17.0.1:55428] "TS.ADD" "humidity:10" "*" "71" "LABELS" "__name__" "humidity" "sensor" "10"
```
