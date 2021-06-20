from storages.backends.s3boto3 import S3Boto3Storage
from .settings.prod import AWS_STORAGE_BUCKET_NAME, STATIC_LOCATION, MEDIA_LOCATION


class StaticStorage(S3Boto3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME
    location = STATIC_LOCATION


class MediaStorage(S3Boto3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME
    location = MEDIA_LOCATION
