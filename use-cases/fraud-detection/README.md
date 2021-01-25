# Building Real Time Fraud Detection Application using Redis 

How to run
1. cd <REDIS_DATASETS_REPO_PATH>/use-cases/fraud-detection/
2. docker build -t redis-fraud:latest . 
3. docker run -e REDIS_HOST='<redis-host>' -e REDIS_PORT=<redis-port> -p 5000:5000 -d redis-fraud

This will run a flask server on port 5000.
3. Sample curl request:
    curl --location --request POST 'localhost:5000' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "device_id": "111-000-000",
        "ip": "1.1.1.2",
        "transaction_id": "3e4fad5fs"
    }'
