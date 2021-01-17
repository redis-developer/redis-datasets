# Building Real Time Fraud Detection Application using Redis 

1. Run redismod docker container
   
2. Run app.py with python3

3. Sample curl:
    curl --location --request POST 'localhost:5000' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "device_id": "111-000-000",
        "ip": "1.1.1.2",
        "transaction_id": "3e4fad5fs"
    }'

Done so far:
1. IP fraud -> lookup cuckoo filter, 
    TODO: add data to filter
   
2. Ad stacked -> using sorted set. 

Todos:
1. Map IP to a location -> use Redis GeoSpatial to get insights on event.
2. Build a bloom filter based device black list db.
3. Send data to stream, read by Redis Gears which will add that data to Redis Time series.
4. Add sample IP blacklist data.