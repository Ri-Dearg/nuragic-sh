"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

from .base import *

try:
    import env  # noqa: F401 # pylint: disable=unused-import
except ModuleNotFoundError:
    # Error handling
    pass


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if DEBUG == 'True':
    print('Debug mode is on.')
elif DEBUG is False:
    print('Debug mode is off.')

ALLOWED_HOSTS = [
    'nuragicshamanichealing.org',
    '157.90.231.34',
    'localhost',
    'nuragic-sh.herokuapp.com',
    '3b4ff521061d4d779f29048eb15db1ed.vfs.cloud9.eu-west-1.amazonaws.com']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR.parent, "static"),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')

# # Settings for AWS bucket
# AWS_S3_OBJECT_PARAMETERS = {
#     'Expires': 'Thu, 31, Dec 2099 20:00:00 GMT',
#     'CacheControl': 'max-age=94608000',
# }

# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = 'eu-west-3'
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'config.custom_storage.StaticStorage'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'

# # Media Settings
# MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'config.custom_storage.MediaStorage'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
