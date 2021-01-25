import os
import redis

from redisbloom.client import Client
from singleton_decorator import singleton


@singleton
class RedisConn:
    def __init__(self):
        host = os.getenv("REDIS_HOST")
        port = os.getenv("REDIS_PORT")

        if not host or not port:
            raise Exception("No Redis Host or Port provided. Please provide Host and Port in docker run command as env")

        port = int(port)
        self.redis_client = redis.Redis(host=host, port=port)
        self.bloom_client = Client(host=host, port=port)

    def redis(self):
        return self.redis_client

    def bloom(self):
        return self.bloom_client
