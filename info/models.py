"""Models for the info module,"""

import datetime
import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from PIL import Image


def image_resize(self, image_title, width, height):
    this_object = None
    image_field = getattr(self, image_title)
    try:
        this_object = self.__class__.objects.get(pk=self.id)
        object_image = getattr(this_object, image_title)
    except self.__class__.DoesNotExist:
        pass
    finally:
        try:
            time = datetime.datetime.strptime('20.12.2016 09:38:42,76',
                                              '%d.%m.%Y %H:%M:%S,%f')
            millisecs = int(time.timestamp() * 1000)
            img = Image.open(image_field)
            img_format = img.format.lower()

            # Prevents images from being copied on every save
            # will save a new copy on an upload
            if (this_object and f'{image_field.name}'
                .replace(' ', '_').replace('(', '').replace(')', '')
                    not in object_image.name) or (not this_object):
                # Image is resized
                output_size = (width, height)
                img = img.resize(size=(output_size))
                # Converts format while in memory
                output = BytesIO()
                img.save(output, format=img_format)
                output.seek(0)

                # Replaces the Imagefield value with the newly converted image
                image_field = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f'{image_field.name.split(".")[0]}_{millisecs}.{img_format}',  # noqa E501
                    'image/jpeg', sys.getsizeof(output),
                    None)
                return image_field
            else:
                return False
        except ValueError:
            return False


class HomeCarousel(models.Model):
    """Allows for the creation of a collection of carousel items.
    You can add a splash image which will be resized and a blurb.
    Images will be resized on upload to 1920x720px square shape.
    I would recommend cropping your images to a 8: 3 ratio first."""
    name = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='carousel')
    display = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        image1 = image_resize(self, 'image', 1920, 720)
        if image1:
            self.image = image1
        super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['-date_added']

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    """Allows for the creation of a collection of Products.
    You can add a splash image which will be resized and a blurb.
    Images will be resized on upload to 1200x628px shape.
    I would recommend cropping your images to a 16: 10 ratio first."""
    title = models.CharField(max_length=30, null=False)
    menu_word = models.CharField(max_length=10, null=False)
    description = models.TextField()
    button_text = models.CharField(max_length=30, null=False)
    image = models.ImageField(upload_to='info/category')
    display = models.BooleanField(default=True)
    order = models.SmallIntegerField(validators=[MaxValueValidator(12),
                                                 MinValueValidator(0)])
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        image1 = image_resize(self, 'image', 1200, 628)
        if image1:
            self.image = image1
        super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['order']
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.menu_word}'


class Page(models.Model):
    """Detailed info for Categories"""
    beige = 'secondary'
    blue = 'info'
    brown = 'brown'
    green = 'success'
    navy = 'primary'
    purple = 'purple'
    red = 'danger'
    yellow = 'warning'

    theme_choices = [(beige, 'beige'),
                     (blue, 'blue'),
                     (brown, 'brown'),
                     (green, 'green'),
                     (navy, 'navy'),
                     (purple, 'purple'),
                     (red, 'red'),
                     (yellow, 'yellow'), ]

    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        related_name='page')
    title = models.CharField(max_length=60, null=False)
    summary = models.CharField(max_length=400, null=False)
    desc_title1 = models.CharField(max_length=60, null=False)
    description1 = models.TextField()
    desc_title2 = models.CharField(max_length=60, blank=True, default='')
    description2 = models.TextField(blank=True, default='')
    title_image = models.ImageField(upload_to='info/page')
    desc_image = models.ImageField(upload_to='info/page')
    bot_image = models.ImageField(upload_to='info/page', blank=True)
    order = models.SmallIntegerField(validators=[MaxValueValidator(12),
                                                 MinValueValidator(0)])
    theme = models.CharField(
        max_length=10, choices=theme_choices, default=blue)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        image1 = image_resize(self, 'title_image', 1500, 500)
        image2 = image_resize(self, 'desc_image', 1200, 628)
        image3 = image_resize(self, 'bot_image', 1500, 500)

        if image1:
            self.title_image = image1

        if image2:
            self.desc_image = image2

        if image3:
            self.bot_image = image3

        super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['order']

    def __str__(self):
        return f'{self.title}'


class GalleryImage(models.Model):
    page = models.ForeignKey(
        Page,
        related_name='gallery',
        default=None,
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='info/page/gallery')

    def __str__(self):
        return f'{self.page}, {self.image}'


class Review(models.Model):
    """Allows for the creation of reviews."""
    reviewer_name = models.CharField(max_length=50, null=False)
    text = models.TextField()
    display = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.reviewer_name}'
