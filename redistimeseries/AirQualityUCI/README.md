# Sample Dataset for AirQuality


Basic time-series setup, using "Air Quality" dataset. 
The Data was recorded from March 2004 to February 2005 (one year) and will enable us to produce the following aggregations using only Redis to do the aggregations and operations on the data.

# How to load the data

## Pre-requisite:
- Install Redismod Docker container

```
docker run -p 6379:6379 redislabs/redismod
```

- Install Python 3.x

```
brew install python3
```

- Cloning the Repositories

```
git clone https://github.com/Redis-Developer/redis-datasets
cd redis-datasets/redistimeseries/
```

- Install Dependencies

```
pip3 install pkg-info
```

```
pip3 install -r requirements.txt
```

## Loading the data

```
python3 dataloader.py 
```

Sample Output:

```
1598021878.806099 [0 172.17.0.1:38436] "ts.add" "ts:carbon_monoxide" "1112596200" "2.4"
1598021878.807271 [0 172.17.0.1:38436] "ts.add" "ts:relative_humidity" "1112596200" "18.3"
1598021878.808320 [0 172.17.0.1:38436] "ts.add" "ts:temperature" "1112599800" "28.3"
1598021878.809399 [0 172.17.0.1:38436] "ts.add" "ts:carbon_monoxide" "1112599800" "2.1"
1598021878.810295 [0 172.17.0.1:38436] "ts.add" "ts:relative_humidity" "1112599800" "13.5"
1598021878.811360 [0 172.17.0.1:38436] "ts.add" "ts:temperature" "1112603400" "28.5"
1598021878.812435 [0 172.17.0.1:38436] "ts.add" "ts:carbon_monoxide" "1112603400" "2.2"
1598021878.813468 [0 172.17.0.1:38436] "ts.add" "ts:relative_humidity" "1112603400" "13.1"
```

## Fetching the Value


```
127.0.0.1:6379> keys *

1) "ts:relative_humidity"
2) "ts:temperature"
3) "ts:carbon_monoxide"
```
