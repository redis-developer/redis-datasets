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


## Demo

Within the scripts folder run > python .\populateTimeSeries.py --sensor-id=10

Then exec into Redis:

```
> docker exec -it db-redis sh
# date +%s
1554591979
# redis-cli
127.0.0.1:6379> TS.RANGE temperature:10 1554591900 1554591979
...
...
...
127.0.0.1:6379> TS.RANGE temperature:10 1554591900 1554591979 AGGREGATION SUM 10
...
127.0.0.1:6379> TS.RANGE temperature:10 1554591900 1554591979 AGGREGATION AVG 10
```
