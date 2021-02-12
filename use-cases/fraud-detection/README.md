# Building Real Time Fraud Detection Application using Redis 


![My Image](https://github.com/redis-developer/redis-datasets/blob/master/use-cases/fraud-detection/Screenshot%202021-01-19%20at%201.50.23%20PM.png)

##  Run redismod docker container or use existing Redis Enterprise

```
docker run -d -p 6379:6379 redislabs/redismod
```

## Cloning the Repository


```
git clone https://github.com/redis-developer/redis-datasets/
```

```
cd redis-datasets/use-cases/fraud-detection/
```

## Building Image

```
docker build -t redis-fraud:latest . 
```

## Running Container

```
docker run -e REDIS_HOST='<redis-host>' -e REDIS_PORT=<redis-port> -p 5000:5000 -d redis-fraud
```

This will start a docker which runs a flask server on port 5000.


## Sample curl:
 
```
curl --request POST 'localhost:5000' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "device_id": "111-000-000",
        "ip": "1.1.1.2",
        "transaction_id": "3e4fad5fs"
    }'
```


## Done so far:

1. IP fraud -> lookup cuckoo filter, 
    TODO: add data to filter
   
2. Ad stacked -> using sorted set. 

### Todos:

1. Map IP to a location -> use Redis GeoSpatial to get insights on event.
2. Build a bloom filter based device black list db.
4. Add sample IP blacklist data.
