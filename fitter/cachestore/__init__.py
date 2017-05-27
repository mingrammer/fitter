class CacheStore(object):
    """Common interface for cache store operations"""
    def get(self):
        raise NotImplementedError('You must implement this method')

    def set(self):
        raise NotImplementedError('You must implement this method')
