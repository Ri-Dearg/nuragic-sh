"""Storages to connect to AWS"""
import json
import os

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class CustomManifestMixin(ManifestFilesMixin):
    """Saves and looks up staticfiles.json in Project directory."""
    manifest_location = os.path.abspath(settings.BASE_DIR)
    manifest_storage = FileSystemStorage(location=manifest_location)

    def read_manifest(self):

        try:
            with self.manifest_storage.open(self.manifest_name) as manifest:
                return manifest.read().decode('utf-8')
        except IOError:
            return None

    def save_manifest(self):
        payload = {'paths': self.hashed_files,
                   'version': self.manifest_version}
        if self.manifest_storage.exists(self.manifest_name):
            self.manifest_storage.delete(self.manifest_name)
        contents = json.dumps(payload).encode('utf-8')
        self.manifest_storage._save(self.manifest_name, ContentFile(contents))


class StaticStorage(  # pylint: disable=abstract-method
        CustomManifestMixin,
        S3Boto3Storage):
    """Sets a custom static file storage for AWS"""
    location = settings.STATICFILES_LOCATION


class MediaStorage(  # pylint: disable=abstract-method
        CustomManifestMixin,
        S3Boto3Storage):
    """Sets a custom media file storage for AWS"""
    location = settings.MEDIAFILES_LOCATION
