from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute


from redis_conn import RedisConn
from constants import Constants


class Setup:

    def init(self):
        self.__register_gears()

    def __register_gears(self):
        # Todo: need better way to check if gears is registered.
        redis_conn = RedisConn().redis()
        is_reg = redis_conn.get("gears_registered")
        if is_reg and int(is_reg) == 1:
            # Gears already registered
            return

        GearsBuilder(reader='StreamReader', r=redis_conn).foreach(lambda x: execute("TS.INCRBY", "clean_ts", 1))\
            .register(Constants.CLEAN_STREAM_NAME)
        GearsBuilder(reader='StreamReader', r=redis_conn).foreach(lambda x: execute("TS.INCRBY", "fraud_ts", 1))\
            .register(Constants.FRAUD_STREAM_NAME)
        redis_conn.set("gears_registered", 1)
