import json

from fitter.cachestore import CacheStore


class InMemoryStore(CacheStore):
    def __init__(self):
        self.kvstore = {}

    def get(self, key):
        return json.loads(self.kvstore[key]) if key in self.kvstore else None

    def set(self, key, value):
        self.kvstore[key] = json.dumps(value)
