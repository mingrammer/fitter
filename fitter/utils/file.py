import hashlib
import os


def generate_hash(param_set):
    _salt_keys = ('mode',
                  'width',
                  'height',
                  'upscale',
                  'quality',
                  'direction',
                  'degree')
    hash_string = param_set.path
    for key in _salt_keys:
        value = param_set.__getattribute__(key)
        if value:
            hash_string += str(value)
    hashed = hashlib.md5(hash_string.encode('utf8')).hexdigest()
    hashed_with_format = '.'.join([hashed, param_set.img_format])
    return hashed_with_format


def get_name_with_ext(path):
    return os.path.basename(path)


def split_name_and_ext(path):
    return os.path.splitext(path)


def get_name_without_ext(path):
    return os.path.splitext(path)[0]


def get_ext(path):
    return os.path.splitext(path)[1]
