# Data Model for Stock Prices and Technical Indicators 

## Pre-requisite

- Clone this Repository

```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redistimeseries/StockPrice
```

- Install Python3
- Install pre-requisite software

```
pip3 install -r requirements.txt
```



## Execute the following command to pull and run the Docker image:

```
docker run -p 6379:6379 -it --rm redislabs/redistimeseries
```

Once you have the Redis TimeSeries container up and running you can connect to the server (make sure you have the right IP address or hostname) using Python script:


```
 % python3 redisTSCreateKeysSample.py 
 % python3 redisTimeSeriesQuerySamples.py 
```



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



 

