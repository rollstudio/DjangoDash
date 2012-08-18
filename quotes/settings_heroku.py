from settings import *

from postgresify import postgresify

DEBUG = False
TEMPLATE_DEBUG = DEBUG

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'citationneeded')
AWS_QUERYSTRING_AUTH = False

DATABASES = postgresify()

STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = STATIC_URL + 'media/'

COMPRESS_ENABLED = DEBUG is False

if COMPRESS_ENABLED:
    COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
    ]
    COMPRESS_STORAGE = 'quotes.utils.CachedS3BotoStorage'
    COMPRESS_URL = STATIC_URL
    COMPRESS_OFFLINE = True


if COMPRESS_ENABLED:
    COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
    ]
    COMPRESS_STORAGE = 'quotes.utils.CachedS3BotoStorage'
    COMPRESS_URL = STATIC_URL
    COMPRESS_OFFLINE = True


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
