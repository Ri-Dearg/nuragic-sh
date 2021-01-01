"""Storages to connect to AWS"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Sets a custom static file storage for AWS"""
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """Sets a custom media file storage for AWS"""
    location = settings.MEDIAFILES_LOCATION
