"""Models for the product module."""

from django.db import models
from django.utils import timezone

from info.models import responsive_images


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
    Images will be resized on upload.
    I would recommend cropping your images first.
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
    image_4_3_md = models.ImageField(default='', blank=True,
                                     upload_to='shop/products')
    image_4_3_sm = models.ImageField(default='', blank=True,
                                     upload_to='shop/products')
    date_added = models.DateTimeField(default=timezone.now)

    stock = models.SmallIntegerField(default=1, blank=False, null=False)
    times_purchased = models.IntegerField(
        default=0, blank=False, null=False, editable=False)
    popularity = models.IntegerField(
        default=0, blank=False, null=False, editable=False)

    def save(self, *args, **kwargs):
        """Generates default stock values.
        Will restock items that are not unique.
        Updates the 'popularity' value.
        Image resizing, snippet repurposed from:
        https://djangosnippets.org/snippets/10597/ """

        image1, image1_md, image1_sm = responsive_images(
            self, 'image_4_3', 945, 1260)

        if image1:
            self.image_4_3 = image1
            self.image_4_3_md = image1_md
            self.image_4_3_sm = image1_sm

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
