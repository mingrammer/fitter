import json

from redis import Redis

from fitter.cachestore import CacheStore


class RedisStore(CacheStore):
    def __init__(self, host, port, db, password):
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
        )

    def get(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value is not None else None

    def set(self, key, value):
        return self.redis.set(key, json.dumps(value))
