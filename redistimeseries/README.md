# Getting Started with RedisTimeSeries

RedisTimeseries is a Redis module developed by Redis Labs to enhance your experience managing time series data with Redis. It simplifies the use of Redis for time-series use cases like IoT, stock prices, and telemetry. With RedisTimeSeries, you can ingest and query millions of samples and events at the speed of Redis. Advanced tooling such as downsampling and aggregation ensure a small memory footprint without impacting performance. Use a variety of queries for visualization and monitoring with built-in connectors to popular tools like Grafana, Prometheus, and Telegraf.

A time series is a linked list of memory chunks. Each chunk has a predefined size of samples. Each sample is a tuple of the time and the value of 128 bits, 64 bits for the timestamp and 64 bits for the value.


In the next steps you will use some basic RedisTimeseries commands, you can run them from the redis-cli or using the CLI available in Redis Insight. (Click on “CLI” in the Redis Insight left menu).
To interact with RedisTimeseries you will most of the time use the TS.RANGE command.

- [AirQualityUCI](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/AirQualityUCI/README.md)
- [Stock Price](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/StockPrice/README.md)
- [Sample Sensors Data](https://github.com/redis-developer/redis-datasets/tree/master/redistimeseries/sample/sensor_data)
- [Sample Python Script to load sensor data](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/sample/python/README.md)
