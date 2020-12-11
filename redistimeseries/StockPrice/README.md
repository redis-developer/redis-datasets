# Data Model for Stock Prices and Technical Indicators (using RedisTimeSeries)

This repository demonstrate a sample code for using RedisTimeSeries to store, aggregate/query stock prices, technical indicators and time-series data sets used by investors. These sets of scripts create various timeseries for prices and indicators. It shows how to create aggregations on top of the raw time series, and demonstrate how easily bulk time series can be ingested and queried using various RedisTimeSeries commands. 

## Pre-requisite

### Clone this Repository

```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redistimeseries/StockPrice
```

###  Install Python3


#### MacOS

```
brew install python3
```

#### Linux

```
apt install python3
```

### Install Prerequisite software

```
pip3 install -r requirements.txt
```



## Running RedisTimeSeries in a Docker Container

```
docker run -p 6379:6379 -it --rm redislabs/redistimeseries
```

Once you have the Redis TimeSeries container up and running you can connect to the server (make sure you have the right IP address or hostname) using Python script:


## Running the scripts

Before running these scripts, ensure that you modify host and port number(6379) for Redis as per your infrastructure setup.

```
 % python3 redisTSCreateKeysSample.py 
 % python3 redisTimeSeriesQuerySamples.py 
```

## Scanning the Keys

```
127.0.0.1:6379> scan 0
1) "15"
2)  1) "INTRADAYPRICES15MINSTDP:GS"
    2) "DAILYRSI:CAT"
    3) "DAILYRSI15MINMAX:GS"
    4) "DAILYRSI15MINMIN:GS"
    5) "INTRADAYPRICES15MINRNG:GS"
    6) "INTRADAYPRICES15MINMIN:GS"
    7) "DAILYRSI15MINLAST:GS"
    8) "INTRADAYPRICES:GS"
    9) "DAILYRSI:GS"
   10) "INTRADAYPRICES15MINMAX:GS"
   11) "DAILYRSI15MINFIRST:GS"
   12) "DAILYRSI15MINRNG:GS"
127.0.0.1:6379> type INTRADAYPRICES15MINSTDP:GS
TSDB-TYPE
127.0.0.1:6379
```

## References

- [Build Your Financial Application on RedisTimeSeries](https://redislabs.com/blog/build-your-financial-application-on-redistimeseries/)
- [Why the Financial Industry Needs Redis Enterprise](https://redislabs.com/blog/why-the-financial-industry-needs-redis-enterprise/)

 

