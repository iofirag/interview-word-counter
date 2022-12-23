import redis

class RedisDriver:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            # init redis connection
            print('RedisDriver will use: ' + host)
            self.pool = redis.ConnectionPool(host=host, port=port, db=db)
            self.redis = redis.Redis(connection_pool=self.pool)
        except:
            print("RedisDriver - Redis connection error")

    def saveWordTs(self, word: str, ts: float):
        return self.redis.lpush(word, ts) # insert at the head

    def getWordTimestampList(self, word: str) -> [float]:
        return self.redis.lrange(word, 0, -1)