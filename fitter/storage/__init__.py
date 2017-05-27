class SourceStorage(object):
    """Common interface for storage as source"""

    def exists(self, key):
        raise NotImplementedError('You must implement this method')

    def get(self, key):
        raise NotImplementedError('You must implement this method')


class StoreStorage(object):
    """Common interface for storage as store"""

    def exists(self, key):
        raise NotImplementedError('You must implement this method')

    def get(self, key):
        raise NotImplementedError('You must implement this method')

    def get_path(self, key):
        raise NotImplementedError('You must implement this method')

    def save(self, key, file):
        raise NotImplementedError('You must implement this method')

    def generate_url(self, key):
        raise NotImplementedError('You must implement this method')
