# Building Pipeline for Natural Language Processing(NLP) using RedisGears

In this tutorial, you will learn how to build a pipeline for Natural Language Processing(NLP) using RedisGears. For this demonstration, we will be leveraging the Kaggle CORD19 datasets. The implementation is designed to avoid running out of memory, leveraging Redis Cluster and Redis Gears, where the use of Redis Gears allows to process data on storage without the need to move data in and out of the Redis cluster. Redis Cluster allows horizontal scalability up to 1000 nodes and together with Redis Gears provides a distributed system where data scientist/ML engineers can focus on processing steps without worry about writing tons of scaffoldings for distributed calculations.



### Step 1. Pre-requisite

Ensure that you install virtualenv in your system


### Step 2. Clone the repository

```
git clone --recurse-submodules https://github.com/applied-knowledge-systems/the-pattern.git
cd the-pattern
```

### Step 3. Bring up the application

```
docker-compose -f docker-compose.dev.yml up --build -d
```

### Step 4. Apply cluster configuration settings

You can deploy PyTorch and spacy to run on RedisGears.

```
bash post_start_dev.sh
```


### Important:

For Data science-focused deployment, RedisCluster should be in HA mode with at least one slave for each master. 
One need to change a few default parameters for rgcluster to accommodate the size of PyTorch and spacy libraries (each over 1GB zipped), gist with settings.
:::


### Step 5. Create or activate Python virtual environment 

```
cd ./the-pattern-platform/
```

### Step 6. Create new environment 

You can create it via 

```
conda create -n pattern_env python=3.8
```
 or 

Alternatively, you can activate by using the below CLI: 

```
source ~/venv_cord19/bin/activate #or create new venv
pip install -r requirements.txt
```

### Step 7. Run pipeline

```
bash cluster_pipeline.sh
```


### Step 8. Validating the functionality of the NLP pipeline

Wait for a bit and then check:

### Verifying Redis Graph populated: 

```
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (n:entity) RETURN count(n) as entity_count" 
redis-cli -p 9001 -h 127.0.0.1 GRAPH.QUERY cord19medical "MATCH (e:entity)-[r]->(t:entity) RETURN count(r) as edge_count"
```
### Checking API responds: 

```
curl -i -H "Content-Type: application/json" -X POST -d '{"search":"How does temperature and humidity affect the transmission of 2019-nCoV"}' http://localhost:8080/gsearch
```

## References

- https://thepattern.digital
