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
cd redis-datasets/redistimeseries/AirQualityUCI/
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



