"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import sys

import dj_database_url
from django.utils.translation import ugettext_lazy as _

try:
    import env  # noqa: F401
except ModuleNotFoundError:
    # Error handling
    pass

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
DEVELOPMENT = os.environ.get('DEVELOPMENT')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)
if DEBUG == 'True':
    print('Debug mode is on.')
elif DEBUG is False:
    print('Debug mode is off.')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'nuragic-sh.herokuapp.com',
                 '3b4ff521061d4d779f29048eb15db1ed.vfs.cloud9.eu-west-1.amazonaws.com']  # noqa E501


# Application definition

INSTALLED_APPS = [
    # Multilingual Model FIelds
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Necessary for allauth
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # App for connecting to AWS
    'storages',
    # Better Array Fields
    'django_better_admin_arrayfield',
    # Apps for compiling SASS
    'sass_processor',
    # Int phone number fields
    'phonenumber_field',
    # Renders form fields
    'crispy_forms',
    # My apps
    'jasmine_testing',
    'contact',
    'info',
    'likes',
    'products',
    'users',
    # Add editor in admin
    'tinymce',
    # Deletes unused media fields
    'django_cleanup.apps.CleanupConfig',
]

SITE_ID = 1

# Settings for SASS compiling
SASS_PRECISION = 8
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
SASS_PROCESSOR_ROOT = 'static/'
COMPRESS_ROOT = 'static'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # for navbar categories
                'info.context_processors.get_categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            # Runs tests on a secondary database
            'NAME': 'dfkr3u5kvd8qj8',
        },
    }
}

# Database config
env_db = dj_database_url.config(conn_max_age=500)

# Declare variable  to check if django is in testing mode
# Uses a test database if True
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
if TESTING:
    env_db = dj_database_url.parse(os.environ.get(
        'HEROKU_POSTGRESQL_CRIMSON_URL'))

# Production Database
DATABASES['default'].update(env_db)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa E501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGES = (
    ('en', _('English')),
    ('it', _('Italian')),
)


LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Checks for the Development variable. If not found it uses AWS.
if not DEVELOPMENT:
    # Settings for AWS bucket
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31, Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }

    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = 'eu-west-3'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'config.custom_storage.StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'

    # Media Settings
    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'config.custom_storage.MediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

# If in development, emails are displayed in the terminal
if 'DEVELOPMENT' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'example@example.com'

# Else emails are sent using real account settings
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

# Settings for Rich Text Editor in admin
TINYMCE_DEFAULT_CONFIG = {
    "height": "280px",
    "width": "960px",
    "plugins": "autosave emoticons link lists preview",
    "toolbar": "undo redo | formatselect fontsizeselect | "
    "bold italic underline | "
    "alignleft aligncenter alignright alignjustify | "
    "numlist bullist | link emoticons | preview restoredraft"
}

# Template pack for crispy_forms.
# Check templates for edits made to bring it in line with bootstrap 5
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_FORMS = {'login': 'users.forms.StyledLoginForm',
                 'signup': 'users.forms.StyledSignupForm',
                 'reset_password': 'users.forms.StyledResetPasswordForm',
                 'reset_password_from_key': 'users.forms.StyledResetPasswordKeyForm',  # noqa E501
                 }
