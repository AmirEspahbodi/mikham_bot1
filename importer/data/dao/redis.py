import redis
from config.redis import RedisConfig
from config.app import AppConfig


class RedisDao:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=RedisConfig.REDIS_HOST,
            port=RedisConfig.REDIS_PORT,
            decode_responses=True,
            encoding="UTF-8",
        )

    def get_importer_break(self):
        return self.redis_client.get(AppConfig.REDIS_IMPORTER_BREAK_KEY)

    def set_importer_break(self, value):
        return self.redis_client.set(AppConfig.REDIS_IMPORTER_BREAK_KEY, value)
