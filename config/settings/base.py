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
from pathlib import Path

import dj_database_url
from django.utils.translation import ugettext_lazy as _

try:
    import env  # noqa: F401 # pylint: disable=unused-import
except ModuleNotFoundError:
    # Error handling
    pass

# Version Number
VERSION = '0.0.6'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parents[2]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

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
    # Better Array Fields
    'django_better_admin_arrayfield',
    # Apps for compiling SASS
    'sass_processor',
    # Int phone number fields
    'phonenumber_field',
    # Renders form fields
    'crispy_forms',
    # My apps
    'cart',
    'checkout',
    'contact',
    'cookies',
    'info',
    'jasmine_testing',
    'likes',
    'policies',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cookies.middleware.DoNotTrackMiddleware',
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
                # Context necessary for shop functions
                'config.context_processors.global_settings',
                'likes.context_processors.get_likes',
                'cart.context_processors.get_cart',
                'policies.context_processors.get_policies',
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
            'NAME': 'd8bgrsa150rjjt',
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
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-pa ssword-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa E501
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa E501
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa E501
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa E501
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

SESSION_COOKIE_AGE = 4838400

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # NOQA: E501

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

    # `allauth` specific authentication methods, such as login by email
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

# Necessary variables and setting to take Stripe Payments.
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')
STRIPE_CURRENCY = 'eur'

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
DEFAULT_FROM_EMAIL = {os.environ.get("EMAIL_HOST_USER")}
DEFAULT_ORDER_EMAIL = {os.environ.get("EMAIL_ORDER")}
DEFAULT_CONTACT_EMAIL = {os.environ.get("EMAIL_CONTACT")}
DEFAULT_ERROR_EMAIL = {os.environ.get("EMAIL_ERROR")}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ADMINS = [('Rory', DEFAULT_ERROR_EMAIL)]
