

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

## Querying via redis-cli

```
redis-cli -h 192.168.1.3 -p 6379
192.168.1.3:6379> FT.SEARCH beerIdx "@abv:[5 6]"
 1) (integer) 1060
 2) "beer:5902"
 3)  1) "brewery"
     2) "DC Brau"
     3) "breweryid"
     4) "1421"
     5) "name"
     6) "The Public"
     7) "category"
     8) "North American Ale"
     9) "categoryid"
    10) "3"
    11) "style"
    12) "American-Style Pale Ale"
    13) "styleid"
    14) "26"
    15) "abv"
    16) "6"
    17) "ibu"
    18) "0"
 4) "beer:5855"
 5)  1) "brewery"
     2) "Half Pints Brewing Company"
     3) "breweryid"
     4) "1401"
     5) "name"
     6) "Little Scrapper IPA"
     7) "category"
     8) "North American Ale"
     9) "categoryid"
    10) "3"
    11) "style"
    12) "American-Style India Pale Ale"
    13) "styleid"
    14) "31"
    15) "abv"
    16) "6"
    17) "ibu"
    18) "0"
 6) "beer:5720"
```


## Querying via RedisInsight

![My Image](https://github.com/redis-developer/redis-datasets/blob/master/redisearch/openbeerdb/images/redisearch.png)
