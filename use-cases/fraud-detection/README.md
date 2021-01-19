# Building Real Time Fraud Detection Application using Redis 

##  Run redismod docker container

```
docker run -d -p 6379:6379 redislabs/redismod
```

## Install pre-requisites

```
pip3 install singleton-decorator-1.0.0
pip3 install redisbloom
pip3 install flask
```
   
##  Run app.py with python3

Clone this repository and run the app.py

```
git clone https://github.com/redis-developer/redis-datasets/
cd redis-datasets/use-cases/fraud-detection/app/
python3 app.py
```

## Sample curl:
 
```
curl --location --request POST 'localhost:5000' \
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
3. Send data to stream, read by Redis Gears which will add that data to Redis Time series.
4. Add sample IP blacklist data.
