from flask import Flask

from config import FitterConfig
from fitter.cachestore.inmemory import InMemoryStore
from fitter.cachestore.redis import RedisStore
from fitter.storage.fs import FileSystemSourceStorage
from fitter.storage.fs import FileSystemStoreStorage
from fitter.storage.s3 import S3SourceStorage
from fitter.storage.s3 import S3StoreStorage


def _set_file_system_storage(storage_class, storage_config):
    return storage_class(
        storage_config['LOCATION'],
        base_url=storage_config.get('BASE_URL'),
    )


def _set_s3_storage(storage_class, storage_config):
    return storage_class(
        storage_config['AWS_ACCESS_KEY_ID'],
        storage_config['AWS_SECRET_ACCESS_KEY'],
        storage_config['BUCKET_NAME'],
        storage_config['BUCKET_REGION'],
        storage_config['LOCATION'],
    )


fitter = Flask('fitter')
fitter.config.from_object(FitterConfig())

fitter.cache_store = None
fitter.source_storage = None
fitter.store_storage = None

if fitter.config['CACHE_STORE']['TYPE'] == 'redis':
    fitter.cache_store = RedisStore(
        fitter.config['CACHE_STORE']['HOST'],
        fitter.config['CACHE_STORE']['PORT'],
        fitter.config['CACHE_STORE']['DB'],
        fitter.config['CACHE_STORE']['PASSWORD'],
    )
elif fitter.config['CACHE_STORE']['TYPE'] == 'in-memory':
    fitter.cache_store = InMemoryStore()

_source_storage_config = fitter.config['SOURCE_STORAGE']
_store_storage_config = fitter.config['STORE_STORAGE']

if _source_storage_config['TYPE'] == 'fs':
    fitter.source_storage = _set_file_system_storage(FileSystemSourceStorage, _source_storage_config)
elif _source_storage_config['TYPE'] == 's3':
    fitter.source_storage = _set_s3_storage(S3SourceStorage, _source_storage_config)

if _store_storage_config['TYPE'] == 'fs':
    fitter.store_storage = _set_file_system_storage(FileSystemStoreStorage, _store_storage_config)
elif _store_storage_config['TYPE'] == 's3':
    fitter.store_storage = _set_s3_storage(S3StoreStorage, _store_storage_config)
