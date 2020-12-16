"""Models for the info module,"""

import sys
from io import BytesIO

from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator

from PIL import Image

from django_better_admin_arrayfield.models.fields import ArrayField


class HomeCarousel(models.Model):
    """Allows for the creation of a collection of carousel items.
    You can add a splash image which will be resized and a blurb.
    Images will be resized on upload to 1920x720px square shape.
    I would recommend cropping your images to a 8:3 ratio first."""
    name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='carousel')
    display = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Image resizing, snippet repurposed from:
        https://djangosnippets.org/snippets/10597/ """
        # Opening the image
        this_object = None
        try:
            this_object = HomeCarousel.objects.get(pk=self.id)
        except HomeCarousel.DoesNotExist:
            pass
        finally:
            img = Image.open(self.image)
            img_format = img.format.lower()

            # Prevents images from being copied on every save
            # will save a new copy on an upload
            if (this_object and self.image.name != this_object.image.name) \
                    or (not this_object):
                # Image is resized
                output_size = (1920, 720)
                img = img.resize(size=(output_size))

                # Converts format while in memory
                output = BytesIO()
                img.save(output, format=img_format)
                output.seek(0)

                # Replaces the Imagefield value with the newly converted image
                self.image = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f'{self.image.name.split(".")[0]}.{img_format}',
                    'image/jpeg', sys.getsizeof(output),
                    None)

                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['-date_added']

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    """Allows for the creation of a collection of Products.
    You can add a splash image which will be resized and a blurb.
    Images will be resized on upload to 1289x480px square shape.
    I would recommend cropping your images to a 16:10 ratio first."""
    name = models.CharField(max_length=30, null=False)
    description = models.TextField()
    button_text = models.CharField(max_length=30, null=False)
    image = models.ImageField(upload_to='info/category')
    display = models.BooleanField(default=True)
    order = models.SmallIntegerField(validators=[MaxValueValidator(12),
                                                 MinValueValidator(0)])
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Image resizing, snippet repurposed from:
        https://djangosnippets.org/snippets/10597/ """
        # Opening the image
        this_object = None
        try:
            this_object = Category.objects.get(pk=self.id)
        except Category.DoesNotExist:
            pass
        finally:
            img = Image.open(self.image)
            img_format = img.format.lower()

            # Prevents images from being copied on every save
            # will save a new copy on an upload
            if (this_object and self.image.name != this_object.image.name) \
                    or (not this_object):
                # Image is resized
                output_size = (1280, 800)
                img = img.resize(size=(output_size))

                # Converts format while in memory
                output = BytesIO()
                img.save(output, format=img_format)
                output.seek(0)

                # Replaces the Imagefield value with the newly converted image
                self.image = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f'{self.image.name.split(".")[0]}.{img_format}',
                    'image/jpeg', sys.getsizeof(output),
                    None)

                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['order']
        verbose_name = 'Categories'

    def __str__(self):
        return f'{self.name}'


class DetailInfo(models.Model):
    """Detailed info for Categories"""
    title = models.CharField(max_length=60, null=False)
    summary = models.CharField(max_length=400, null=False)
    description1 = models.TextField()
    description2 = models.TextField(blank=True, default='')
    title_image = models.ImageField(upload_to='info/detail/title')
    desc_image = models.ImageField(upload_to='info/detail/desc', blank=True)


class GalleryImage(models.Model):
    detail = models.ForeignKey(
        DetailInfo, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='info/detail/gallery')


class Review(models.Model):
    """Allows for the creation of reviews."""
    reviewer_name = models.CharField(max_length=50, null=False)
    text = models.TextField()
    display = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.reviewer_name}'
