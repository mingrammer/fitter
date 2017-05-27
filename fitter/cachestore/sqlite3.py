import sqlite3

from fitter.cachestore import CacheStore


class SQLite3Store(CacheStore):
    def __init__(self):
        self.sqlite3 = sqlite3.connect(':memory:')

    def get(self, key):
        # TODO: Supports in-memory cache
        pass

    def set(self, key, value):
        # TODO: Supports in-memory cache
        pass
