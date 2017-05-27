import os

import boto3
from botocore.exceptions import ClientError

from fitter.storage import SourceStorage, StoreStorage


class S3Storage(object):
    """A simple wrapper of AWS S3"""

    AVAIABLE_REGIONS = (
        'us-gov-west-1',
        'us-east-1',
        'us-west-1',
        'us-west-2',
        'eu-west-1',
        'eu-central-1,'
        'ap-northeast-1',
        'ap-northeast-2',
        'ap-southeast-1',
        'sa-east-1',
        'cn-north-1',
    )

    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, region_name, location):
        self.client = boto3.client('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   region_name=region_name)
        self.bucket_name = bucket_name
        self.location = location

    @classmethod
    def is_valid_region(cls, region_name):
        if region_name in cls.AVAIABLE_REGIONS:
            return True
        return False


class S3SourceStorage(S3Storage, SourceStorage):
    def __init__(self, *args, **kwargs):
        super(S3SourceStorage, self).__init__(*args, **kwargs)

    def exists(self, key):
        try:
            self.client.head_object(Bucket=self.bucket_name,
                                    Key=os.path.join(self.location, key))
            return True
        except ClientError:
            return False

    def get(self, key):
        obj = self.client.get_object(Bucket=self.bucket_name,
                                          Key=os.path.join(self.location, key))
        return obj['Body']


class S3StoreStorage(S3Storage, StoreStorage):
    def __init__(self, *args, **kwargs):
        super(S3StoreStorage, self).__init__(*args, **kwargs)
        self.cache_location = os.path.join('cache', self.location.strip('/'))

    def exists(self, key):
        try:
            self.client.head_object(Bucket=self.bucket_name,
                                    Key=os.path.join(self.cache_location, key))
            return True
        except ClientError:
            return False

    def get(self, key):
        obj = self.client.get_object(Bucket=self.bucket_name,
                                          Key=os.path.join(self.cache_location, key))
        return obj['Body']

    def get_path(self, key):
        return os.path.join(self.cache_location,
                            key)

    def save(self, key, file):
        self.client.put_object(Bucket=self.bucket_name,
                               Key=os.path.join(self.cache_location, key),
                               Body=file)
        return key

    def generate_url(self, key):
        url = os.path.join(self.client.meta.endpoint_url,
                           self.bucket_name,
                           self.cache_location,
                           key)
        return url
