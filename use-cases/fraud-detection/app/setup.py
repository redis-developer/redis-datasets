from gearsclient import GearsRemoteBuilder as GearsBuilder

from redis_conn import RedisConn

import os
import json
import redis
from redistimeseries.client import Client


class Setup:

    def init(self):
        self.__register_gears()

    def __register_gears(self):
        redis_conn = RedisConn().redis()
        is_reg = redis_conn.get("gears_registered")
        if is_reg and int(is_reg) == 1:
            # Gears already registered
            return

        def stream_handler(item):
            data = item['value']
            member = json.dumps(
                {'device_id': data['device_id'],
                 'transaction_id': data['transaction_id'],
                 'ts': data['ts'],
                 })
            redis.Redis().zadd(data.get('device_id'), {member: data['ts']})
            Client().incrby(data['fraud_type'], 1)

        GearsBuilder(reader='StreamReader', r=redis_conn, requirements=["redis", "redistimeseries"]).foreach(stream_handler).register('data_stream')
        # To avoid multiple gears from being registered for single use case, set this when register is done,
        # unset this if you want to re-register the Gear when application runs again.
        redis_conn.set("gears_registered", 1)