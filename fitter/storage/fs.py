import io
import os

import requests

from fitter.storage import SourceStorage
from fitter.storage import StoreStorage


class FileSystemStorage(object):
    """A simple wrapper of file system"""

    def __init__(self, location, base_url=None):
        self.location = location
        self.base_url = base_url


class FileSystemSourceStorage(FileSystemStorage, SourceStorage):
    def __init__(self, *args, **kwargs):
        super(FileSystemSourceStorage, self).__init__(*args, **kwargs)

    def exists(self, key):
        if os.path.isfile(os.path.join(self.location, key)):
            return True
        return False

    def get(self, key):
        file_obj = open(os.path.join(self.location, key), 'rb')
        return file_obj


class FileSystemStoreStorage(FileSystemStorage, StoreStorage):
    def __init__(self, *args, **kwargs):
        super(FileSystemStoreStorage, self).__init__(*args, **kwargs)
        self.cache_location = os.path.join('cache', self.location.strip('/'))

    def exists(self, key):
        url = self.generate_url(key)
        result = requests.get(url, stream=True)
        return result.status_code == 200

    def get(self, key):
        url = self.generate_url(key)
        result = requests.get(url, stream=True)
        with io.StringIO() as file_obj:
            for chunk in result:
                file_obj.write(chunk)
            return file_obj

    def get_path(self, key):
        return os.path.join(self.cache_location,
                            key)

    def save(self, key, file):
        files = {'file': (key, file.getvalue())}
        result = requests.post(
            os.path.join(self.base_url, self.cache_location),
            files=files,
        )
        if result.status_code != 201:
            raise Exception('Can\'t upload the given image')
        return key

    def generate_url(self, key):
        return os.path.join(self.base_url,
                            self.cache_location,
                            key)
