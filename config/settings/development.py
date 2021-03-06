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

DEVELOPMENT = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if DEBUG == 'True':
    print('Debug mode is on.')
elif DEBUG is False:
    print('Debug mode is off.')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # noqa E501

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
