import redis
from config.redis import RedisConfig


class RedisDao:
    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=RedisConfig.REDIS_HOST,
            port=RedisConfig.REDIS_PORT,
            decode_responses=True,
            encoding="UTF-8",
        )

    def dequeue(
        self, queue_name=RedisConfig.REDIS_SLEEP_GOOGLE_MAP_SEARCH_QUERIES
    ):
        if self.redis_client.exists(queue_name):
            search_query = self.redis_client.lpop(queue_name)
            return search_query
        return None

    def set_inprocessing(self, search_query):
        self.redis_client.set(
            RedisConfig.REDIS_GOOGLE_MAP_IN_PROCESSING_SEARCH_QUERY, search_query
        )

    def remove_inprocessing(self):
        self.redis_client.delete(
            RedisConfig.REDIS_GOOGLE_MAP_IN_PROCESSING_SEARCH_QUERY
        )
