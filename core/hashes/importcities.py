import csv
import config
from redis import Redis

# Database Connection
host = config.REDIS_CFG["host"]
port = config.REDIS_CFG["port"]
pwd = config.REDIS_CFG["password"]
redis = Redis(host=host, port=port, password=pwd, charset="utf-8", decode_responses=True)

# Import Cities
print("Importing ...")

count = 0

with open("data/worldcities.csv", 'r') as cities:
    reader = csv.DictReader(cities)
    for row in reader:
        id = row["id"]
        name = row["city_ascii"]
        lng = row["lng"]
        lat = row["lat"]
        country = row["country"]
        pop = row["population"]

        print("id = {}, name = {}, lng = {}, lat = {}".format(id, name, lng, lat))
        count += 1

        redis.hmset("ct:{}".format(id), { "_id" : id, "name" : name, "country" : country, "population" : pop })
        redis.geoadd("idx:cities", lng, lat, id)
        redis.hset("idx:city_by_name", name, id)
