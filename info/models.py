"""Models for the info module,"""

import sys
from io import BytesIO

from django.db import models
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator

from PIL import Image

from django_better_admin_arrayfield.models.fields import ArrayField


def image_resize(self, image_title, folder, width, height):
    this_object = None
    image_field = getattr(self, image_title)
    try:
        this_object = self.__class__.objects.get(pk=self.id)
        object_image = getattr(this_object, image_title)
    except self.__class__.DoesNotExist:
        pass
    finally:
        try:
            img = Image.open(image_field)
        except ValueError:
            img = None
            return True
        finally:
            if img:
                img_format = img.format.lower()

                # Prevents images from being copied on every save
                # will save a new copy on an upload
                if (this_object and f'{folder}' + '/' + f'{image_field.name}'.replace(" ", "_")
                        != object_image.name) or (not this_object):
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
                        f'{image_field.name.split(".")[0]}.{img_format}',
                        'image/jpeg', sys.getsizeof(output),
                        None)
                    return True
                else:
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
        if image_resize(self, 'image', 'info/carousel', 1920, 720) is False:
            super().save(*args,
                         update_fields=['name', 'description', 'display'],
                         **kwargs)
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
    I would recommend cropping your images to a 16: 10 ratio first."""
    name = models.CharField(max_length=30, null=False)
    menu_word = models.CharField(max_length=10, null=False)
    description = models.TextField()
    button_text = models.CharField(max_length=30, null=False)
    image = models.ImageField(upload_to='info/category')
    display = models.BooleanField(default=True)
    order = models.SmallIntegerField(validators=[MaxValueValidator(12),
                                                 MinValueValidator(0)])
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if image_resize(self, 'image', 'info/category', 1280, 800) is False:
            super().save(*args,
                         update_fields=['name', 'menu_word', 'description',
                                        'button_text', 'display', 'order'],
                         **kwargs)
        else:
            super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['order']
        verbose_name = 'Categorie'

    def __str__(self):
        return f'{self.name}'


class DetailInfo(models.Model):
    """Detailed info for Categories"""
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=60, null=False)
    summary = models.CharField(max_length=400, null=False)
    description1 = models.TextField()
    description2 = models.TextField(blank=True, default='')
    title_image = models.ImageField(upload_to='info/detail')
    desc_image = models.ImageField(upload_to='info/detail', blank=True)
    order = models.SmallIntegerField(validators=[MaxValueValidator(12),
                                                 MinValueValidator(0)])
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        update_fields = ['category', 'title', 'summary',
                         'description1', 'description2', 'order',
                         'date_added', 'title_image', 'desc_image']

        image1 = image_resize(self, 'title_image', 'info/detail', 1920, 720)
        image2 = image_resize(self, 'desc_image', 'info/detail', 1280, 800)
        if image1 is False:
            update_fields = update_fields.remove('title_image')
        if image2 is False:
            update_fields = update_fields.remove('desc_image')

        if (image1 or image2) is False:
            super().save(*args, update_fields=update_fields, **kwargs)
        else:
            super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['order']

    def __str__(self):
        return f'{self.title}'


class GalleryImage(models.Model):
    detail = models.ForeignKey(
        DetailInfo, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='info/detail/gallery')

    def __str__(self):
        return f'{self.detail}, {self.image}'


class Review(models.Model):
    """Allows for the creation of reviews."""
    reviewer_name = models.CharField(max_length=50, null=False)
    text = models.TextField()
    display = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.reviewer_name}'
