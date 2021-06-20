# File contains Django production settings for ePromotor project.

import dj_database_url
from .base import env

db_from_env = dj_database_url.config(conn_max_age=500)

# Remote database config
DATABASES = {
    'default': db_from_env
}

# S3 buckets config
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_REGION = env('AWS_REGION')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    AWS_STORAGE_BUCKET_NAME, AWS_REGION)

STATIC_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATIC_LOCATION)

MEDIA_LOCATION = 'media'
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIA_LOCATION)

STATICFILES_STORAGE = 'ePromotor.custom_storage.StaticStorage'
DEFAULT_FILE_STORAGE = 'ePromotor.custom_storage.MediaStorage'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None


# Additional options
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
