"""Models for the product module."""

import datetime
import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from PIL import Image


def image_resize(self, image_title, width, height):
    """Function to resize the images for smaller memory."""
    # Checks if the instance already exists
    this_object = None
    image_field = getattr(self, image_title)
    try:
        # If it exists, selects current image, if not goes to next step
        this_object = self.__class__.objects.get(pk=self.id)
        object_image = getattr(this_object, image_title)
    except self.__class__.DoesNotExist:
        pass
    finally:
        try:
            # Makes each image unique, django-cleanup deletes shared files
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
            # if the image doesn't need to be changed, returns false
            else:
                return False
        # If uploading multiple images on a new file there can this error.
        except ValueError:
            return False


class ShopCategory(models.Model):
    """Defines categories to apply to products.
    A simple model to group products."""
    title = models.CharField(max_length=254)
    display = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Shop Categories'
        ordering = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    """Defines the Product Class. Many fields are optional.
    A default image is uploaded if no image is selected.
    Images will be resized on upload to 500x500px square shape.
    I would recommend cropping your images to a 1:1 ratio first.
    It automatically sets stock values based on is_unique value.
    Generates the 'popularity' value on save.This value is a combination of the
    total quantity an item was sold and how many unique users have liked it."""

    category = models.ForeignKey(ShopCategory,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='products')

    title = models.CharField(max_length=254, default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_4_3 = models.ImageField(default='default.jpg',
                                  upload_to='shop/products')
    date_added = models.DateTimeField(default=timezone.now)

    stock = models.SmallIntegerField(default=1, blank=False, null=False)
    times_purchased = models.IntegerField(
        default=0, blank=False, null=False, editable=False)
    popularity = models.IntegerField(
        default=0, blank=False, null=False, editable=False)

    def save(self, *args, **kwargs):
        """ Generates default stock values.
        Will restock items that are not unique.
        Updates the 'popularity' value.
        Image resizing, snippet repurposed from:
        https://djangosnippets.org/snippets/10597/ """

        image1 = image_resize(self, 'image_4_3', 960, 1280)

        if image1:
            self.image = image1

        # Updates popularity (See below)
        # self._update_popularity()

        super().save(*args, **kwargs)

    # def _update_popularity(self):
    #     """Used for item ordering so more popular items are displayed first.
    #     A combination of total unique likes and number sold."""
    #     self.popularity = self.users.count() + self.times_purchased

    class Meta:
        ordering = ['-popularity']

    def __str__(self):
        return f'{self.title}: €{self.price}'
