import redis.asyncio as redis

class RedisDriver:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            # init redis connection
            print('RedisDriver will use: ' + host)
            self.pool = redis.ConnectionPool(host=host, port=port, db=db)
            self.redis = redis.Redis(connection_pool=self.pool)
        except:
            print("RedisDriver - Redis connection error")

    async def save_word_ts(self, word: str, ts: float) -> None:
        return await self.redis.lpush(word, ts) # insert at the head

    async def get_word_ts_list(self, word: str) -> [float]:
        return await self.redis.lrange(word, 0, -1)