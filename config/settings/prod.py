"""Django settings when running project in production."""
from .base import * # noqa

ALLOWED_HOSTS = [
    '.execute-api.us-east-2.amazonaws.com',
    '.rjifuture.org',
    '.tweetstotext.io',
]

INSTALLED_APPS = INSTALLED_APPS + ['storages', ]

AWS_ACCESS_KEY_ID = secrets.get('aws_access_key_id')
AWS_SECRET_ACCESS_KEY = secrets.get('aws_secret_access_key')
AWS_S3_REGION_NAME = secrets.get('aws_region_name')
AWS_AUTO_CREATE_BUCKET = True
AWS_BUCKET_ACL = 'public-read'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
AWS_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_STATIC_BUCKET_NAME = 'tweets2text'
AWS_STATIC_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STATIC_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_STATIC_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'config.settings.storage_backends.StaticStorage'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
