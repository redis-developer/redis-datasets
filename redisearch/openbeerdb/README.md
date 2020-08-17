

# Redis Beer Database Sample Dataset


- This dataset contains openbeerdb data.
- Search for your favourite beer in the beer index. 
- Add an alias to the index and query the alias for your favourite beer

Link: https://openbeerdb.com/

This dataset could be used for:

- RediSearch

## Tested Infra

- MacOS running redis server compiled  with Redisearch modules


## Cloning the Repository

```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redisearch/openbeerdb/beerloader
```

## Installing Pre-requisites:

```
brew install python3
pip3 install -r requirements.txt
```

## Importing the data

```
python3 import.py --url redis://192.168.1.3:6379
```


## Querying via RedisInsight

![My Image](https://github.com/redis-developer/redis-datasets/blob/master/redisearch/openbeerdb/images/redisearch.png)
