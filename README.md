# A Curated List of Sample Redis Datasets

This page shows the sample datasets available for Redis Modules. Click the below sample dataset to lean more about it.



## [RediSearch](https://github.com/redis-developer/redis-datasets/blob/master/redisearch/README.md)


| List of Dataset | Description |
| --- | --- |
| [Movie Dataset](https://github.com/Redis-Developer/redis-datasets/tree/movie-dataset/movie-database) | Contains details on Movie Database listings |
| [OpenBeerDB](https://github.com/Redis-Developer/redis-datasets/tree/master/redisearch/openbeerdb) | Contains details on Openbeer listings |
| [User Sample Datasets](https://github.com/redis-developer/redis-datasets/blob/master/user-database/README.md) | Contains details on Openbeer listings |


## [RedisGraph](https://github.com/redis-developer/redis-datasets/blob/master/redisgraph/README.md)

| List of Dataset | Description |
| --- | --- |
| [An API of Ice and Fire](https://github.com/Redis-Developer/redis-datasets/blob/master/redisgraph/datasets/iceandfire/README.md) | Contains details on Ice & Fire API Database listings |
| [Movie Dataset](https://github.com/Redis-Developer/redis-datasets/tree/movie-dataset/movie-database) | Contains details on Movie Database listings |
| [Redis Graph Bulk Loader](https://github.com/Redis-Developer/redis-datasets/tree/master/redisgraph/redisgraph-bulk-loader) | Loading bulk data into Redisgraph |

## RedisGears

| List of Dataset | Description |
| --- | --- |
| [Sample IMDB Dataset](https://github.com/Redis-Developer/redis-datasets/blob/master/redisgears/README.md) | Contains details on IMDB Movie Database listings |



## [RedisJSON](https://github.com/redis-developer/redis-datasets/blob/master/redisjson/README.md)

| List of Dataset | Description |
| --- | --- |
| [Employee Profile dataset](https://github.com/redis-developer/redis-datasets/blob/master/redisjson/README.md) | Contains details on Sample Employee Profile Database listings |
| Sample Dataset | Contains details on Sample listings |



## [RedisTimeseries](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/README.md)

| List of Dataset | Description |
| --- | --- |
| [AirQuality Dataset](https://github.com/Redis-Developer/redis-datasets/tree/master/redistimeseries/AirQualityUCI) | Contains details on Air Quality listings |
| [Stock Price Dataset](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/StockPrice/README.md) | Data model for stock prices |


## [RedisAI](https://github.com/redis-developer/redis-datasets/blob/master/redisai/README.md)


| List of Dataset | Description |
| --- | --- |
| [Animal Recognition Demo](https://github.com/RedisGears/AnimalRecognitionDemo) | Contains details on Animal Recognition datasets |
| [Edge Real time Video Analytics](https://github.com/RedisGears/EdgeRealtimeVideoAnalytics)| Contains details on Edge Real time Video Analytics datasets |
| [Chat Bot Demo](https://github.com/RedisAI/ChatBotDemo) | Contains details on Chat Bot Demo datasets |
[ Redis AI Showcase](https://github.com/RedisAI/redisai-examples) | Contains details on Redis AI Showcase datasets|

## [RedisBloom](https://github.com/redis-developer/redis-datasets/blob/master/redisbloom/README.md)

| List of Dataset | Description |
| --- | --- |
| [Unique Website Visitor](https://github.com/redis-developer/redis-datasets/blob/master/redisbloom/README.md) | Contains details on Unique IP address visitors listings |



## How to test drive these Modules For FREE !!

<details><summary>
Using Redis Cloud
  </summary>

<br>
Sign up for a free account [here](https://redislabs.com/redis-enterprise-cloud/) and get 30MB free tier at $0. Use the button below to register yourself and get started in no seconds. 


</details>

[![](https://github.com/Redis-Developer/redis-datasets/blob/master/images/recloud.png)](https://app.redislabs.com/#/add-subscription)

<details><summary>
Using Linux
</summary>
  
Following are the pre-requisites for using Redis Modules



#### Installing Redis
Reference and more detailed steps: [here](https://redis.io/download#installation)

```bash
$ wget http://download.redis.io/redis-stable.tar.gz

$ tar xvzf redis-stable.tar.gz

$ cd redis-stable

$ make

$ make test

$ sudo make install
```
</details>


<details><summary>
Build RedisGraph Module(Example)
</summary>

  
Reference and more detailed steps: [here](https://oss.redislabs.com/redisgraph/)

```bash
# Ubuntu/Linux

$ sudo apt-get install build-essential cmake m4 automake peg libtool autoconf

# Mac

$ brew install cmake m4 automake peg libtool autoconf

$ git clone --recurse-submodules -j8 [https://github.com/RedisGraph/RedisGraph.git](https://github.com/RedisGraph/RedisGraph.git)

$ cd RedisGraph

$ make
```
</details>

<details><summary>
Using Docker
</summary>
  
```
docker run -p 6379:6379 redislabs/redismod
```

```
redis-cli -h localhost
```

```
# Modules
module:name=ft,ver=10613,api=1,filters=0,usedby=[],using=[],options=[]
module:name=rg,ver=10001,api=1,filters=0,usedby=[],using=[ai],options=[]
module:name=bf,ver=20204,api=1,filters=0,usedby=[],using=[],options=[]
module:name=ReJSON,ver=10004,api=1,filters=0,usedby=[],using=[],options=[]
module:name=ai,ver=10001,api=1,filters=0,usedby=[rg],using=[],options=[]
module:name=graph,ver=20019,api=1,filters=0,usedby=[],using=[],options=[]
module:name=timeseries,ver=10207,api=1,filters=0,usedby=[],using=[],options=[]

# Cluster
cluster_enabled:0

# Keyspace
db0:keys=1,expires=0,avg_ttl=0
localhost:6379> info
```
  
</details>



