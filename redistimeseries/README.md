# Getting Started with RedisTimeSeries

RedisTimeseries is a Redis module developed by Redis Labs to enhance your experience managing time series data with Redis. It simplifies the use of Redis for time-series use cases like IoT, stock prices, and telemetry. With RedisTimeSeries, you can ingest and query millions of samples and events at the speed of Redis. Advanced tooling such as downsampling and aggregation ensure a small memory footprint without impacting performance. Use a variety of queries for visualization and monitoring with built-in connectors to popular tools like Grafana, Prometheus, and Telegraf.
A time series is a linked list of memory chunks. Each chunk has a predefined size of samples. Each sample is a tuple of the time and the value of 128 bits, 64 bits for the timestamp and 64 bits for the value.


In the next steps you will use some basic RedisTimeseries commands, you can run them from the redis-cli or using the CLI available in Redis Insight. (Click on “CLI” in the Redis Insight left menu).
To interact with RedisTimeseries you will most of the time use the TS.RANGE command.
You will create a very basic AirQuality datasets you will see how to:

- Create a new time-series
- Adding a new sample to the list of series
- Query a range across one or multiple time-series


## Create a new time-series

Let’s create a time series representing AirQuality dataset measurements. You will create a time series per measurement using TS.CREATE. Once created all the measurements will be sent using TS.ADD.
The below sample creates a time series and populates it with three entries.

```
>> TS.CREATE ts:carbon_monoxide
>> TS.CREATE ts:relative_humidity

>> TS.CREATE ts:temperature RETENTION 60 LABELS sensor_id 2 area_id 32
```


In the above example, ts:carbon_monoxide, ts:relative_humidity & ts:temperature are key names. 
In the above  example, we are creating a time series with two labels (sensor_id and area_id are the fields with values 2 and 32 respectively) and 
a retention window of 60 milliseconds:


## 1.1 Adding a new sample data to the time-series

Let’s start to add samples into the keys that will be automatically created during this command.

```
>> TS.ADD ts:carbon_monoxide 1112596200 2.4
>> TS.ADD ts:relative_humidity 1112596200 18.3
>> TS.ADD ts:temperature 1112599800 28.3
```

```
>> TS.ADD ts:carbon_monoxide 1112599800 2.1
>> TS.ADD ts:relative_humidity 1112599800 13.5
>> TS.ADD ts:temperature 1112603400 28.5 
```

```
>> TS.ADD ts:carbon_monoxide 1112603400 2.2
>> TS.ADD ts:relative_humidity 1112603400 13.1
>> TS.ADD ts:temperature 1112607000 28.7
```

## 1.2 Querying the sample 

Now that you have sample data in your timeseries it is time to ask questions such as:

### “How shall I get the last sample?”

TS.GET is used to get the last sample. The returned array will contain the last sample timestamp followed by the last sample value, when the time-series contains
data. 


```
>> TS.GET ts:temperature
1) (integer) 1112607000
2) "28.7"
```

### “How shall I get the last sample matching the specific filter?”

TS.MGET is used to get the last samples matching the specific filter.

```
>> TS.MGET FILTER area_id=32
1) 1) "ts:temperature"
   2) (empty list or set)
   3) 1) (integer) 1112607000
      2) "28.7"
```

### “How shall I get the sample with labels matching the specific filter?”

```
>> TS.MGET WITHLABELS FILTER area_id=32
1) 1) "ts:temperature"
   2) 1) 1) "sensor_id"
         2) "2"
      2) 1) "area_id"
         2) "32"
   3) 1) (integer) 1112607000
      2) "28.7"
```

## 1.3 Query a range across one or multiple time-series

```
>> TS.RANGE ts:carbon_monoxide 1112596200 1112603400
1) 1) (integer) 1112596200
   2) "2.4"
2) 1) (integer) 1112599800
   2) "2.1"
3) 1) (integer) 1112603400
   2) "2.2"

## 1.4  Aggregation


```
>> TS.RANGE ts:carbon_monoxide 1112596200 1112603400 AGGREGATION avg 2
1) 1) (integer) 1112596200
   2) "2.4"
2) 1) (integer) 1112599800
   2) "2.1"
3) 1) (integer) 1112603400
   2) "2.2"
```
