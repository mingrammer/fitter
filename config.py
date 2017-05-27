import sys

import yaml

from fitter.storage.s3 import S3Storage
from fitter.utils.print import eprint


class _CacheStoreConfig:
    _class = 'cache_store'

    def as_dict(self):
        return self.__dict__


class InMemoryCacheStoreConfig(_CacheStoreConfig):
    def __init__(self, **kwargs):
        self.TYPE = 'in-memory'

    def as_dict(self):
        return self.__dict__


class RedisCacheStoreConfig(_CacheStoreConfig):
    def __init__(self, **kwargs):
        self.TYPE = 'redis'
        self.HOST = kwargs.get('host', 'localhost')
        self.PORT = kwargs.get('port', 6379)
        self.DB = kwargs.get('db', 0)
        self.PASSWORD = kwargs.get('password', None)

    def as_dict(self):
        return self.__dict__


class _StorageConfig:
    _class = 'storage'

    def as_dict(self):
        return self.__dict__


class FileSystemStorageConfig(_StorageConfig):
    def __init__(self, location, **kwargs):
        self.TYPE = 'fs'
        self.LOCATION = location
        self.BASE_URL = kwargs.get('base_url')


class S3StorageConfig(_StorageConfig):
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, bucket_region, location, **kwargs):
        if not S3Storage.is_valid_region(bucket_region):
            eprint('\'{}\' region is not valid for S3'.format(bucket_region))
            sys.exit(-1)
        self.TYPE = 's3'
        self.AWS_ACCESS_KEY_ID = aws_access_key_id
        self.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
        self.BUCKET_NAME = bucket_name
        self.BUCKET_REGION = bucket_region
        self.LOCATION = location


class OptionsConfig:
    def __init__(self, **kwargs):
        self.ENABLE_UPLOAD = kwargs.get('enable_upload', False)
        self.ENABLE_HASH = kwargs.get('enable_hash', False)

    def as_dict(self):
        return self.__dict__


class FitterConfig:
    _CONFIG_FILE = 'fitter.yaml'

    CACHE_STORE = None
    SOURCE_STORAGE = None
    STORE_STORAGE = None
    OPTIONS = None

    def __init__(self):
        config = self._load_config_file()
        self.PORT = config.get('port', 6001)
        self.SECRET_KEY = config.get('secret_key', None)
        # Cache store is optional field
        if 'cache_store' in config:
            self._load_cache_store_config(config['cache_store'])
        # Options is optional field
        if 'options' in config:
            self._load_options_config(config['options'])
        # Storage is required field
        if 'storage' in config:
            self._load_storage_config(config['storage'])
        else:
            eprint('You must set the \'storage\' config')
            sys.exit(-1)

    def _load_config_file(self):
        try:
            config = yaml.load(open(self._CONFIG_FILE, 'r'))
            return config
        except IOError:
            eprint('You need \'fitter.yaml\' for fitter configuration')
            sys.exit(0)

    @staticmethod
    def _validate_cache_store_fields(cache_store_config):
        _required_fields = ('type',)
        if not all(map(lambda e: e in cache_store_config, _required_fields)):
            eprint('There are some missing values for cache store: one of {}'.format(_required_fields))
            return False
        if cache_store_config['type'] not in ('redis', 'in-memory'):
            eprint('\'{}\' is not supported type for cache store'.format(cache_store_type))
            return False
        return True

    def _load_cache_store_config(self, cache_store_config):
        if not self._validate_cache_store_fields(cache_store_config):
            sys.exit(-1)
        cache_store_type = cache_store_config['type']
        if cache_store_type == 'redis':
            self.CACHE_STORE = RedisCacheStoreConfig(**cache_store_config).as_dict()
        if cache_store_type == 'in-memory':
            self.CACHE_STORE = InMemoryCacheStoreConfig(**cache_store_config).as_dict()

    @staticmethod
    def _validate_storage_fields(storage_config):
        _required_fields = ('type',)
        _required_fields_for_fs_storage = ('location',)
        _required_fields_for_s3_storage = (
            'aws_access_key_id', 'aws_secret_access_key', 'bucket_name', 'bucket_region', 'location')
        if not all(map(lambda e: e in storage_config, _required_fields)):
            eprint('There are some missing values for storage: one of {}'.format(_required_fields))
            return False
        if storage_config['type'] == 'fs':
            if not all(map(lambda e: e in storage_config, _required_fields_for_fs_storage)):
                eprint('There are some missing values of \'file system\' backed storage')
                return False
        elif storage_config['type'] == 's3':
            if not all(map(lambda e: e in storage_config, _required_fields_for_s3_storage)):
                eprint('There are some missing values of \'s3\' backed storage')
                return False
        else:
            eprint('{} is not supported storage type'.format(storage_config['type']))
            return False
        return True

    @staticmethod
    def _choose_storage_type(single_storage_config):
        storage_type = single_storage_config['type']
        if storage_type == 'fs':
            return FileSystemStorageConfig(**single_storage_config).as_dict()
        elif storage_type == 's3':
            return S3StorageConfig(**single_storage_config).as_dict()

    def _load_storage_config(self, storage_config):
        if 'store' not in storage_config:
            eprint('You must set the \'store\' of \'storage\'')
            sys.exit(0)
        if 'source' in storage_config:
            if not self._validate_storage_fields(storage_config['source']):
                sys.exit(0)
            if not self._validate_storage_fields(storage_config['store']):
                sys.exit(0)
            source_config = storage_config['source']
            store_config = storage_config['store']
        else:
            if not self._validate_storage_fields(storage_config['store']):
                sys.exit(0)
            source_config = storage_config['store']
            store_config = storage_config['store']
        self.SOURCE_STORAGE = self._choose_storage_type(source_config)
        self.STORE_STORAGE = self._choose_storage_type(store_config)

    def _load_options_config(self, options_config):
        self.OPTIONS = OptionsConfig(**options_config).as_dict()
