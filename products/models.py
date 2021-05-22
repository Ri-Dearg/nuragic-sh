"""Models for the product module."""

from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from tinymce.models import HTMLField

from info.utils import responsive_images


class ShopCategory(models.Model):
    """Defines categories to apply to products.
    A simple model to group products."""
    title = models.CharField(max_length=50)
    display = models.BooleanField(default=True)
    slug = models.SlugField(
        default='', editable=False, max_length=50, null=False)

    def get_absolute_url(self):
        """Adds slug to url for page redirection."""
        kwargs = {'slug': self.slug,
                  'pk': self.id
                  }
        return reverse('products:shop-category-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        """Generates a slug for the url."""
        slug_value_en = self.title_en
        self.slug_en = slugify(slug_value_en, allow_unicode=True)

        slug_value_it = self.title_it
        self.slug_it = slugify(slug_value_it, allow_unicode=True)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Shop Categories'
        ordering = ['title']

    def __str__(self):
        return str(self.title)


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
    description = HTMLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_cost = models.DecimalField(
        default=6.99, max_digits=10, decimal_places=2)
    image_4_3 = models.ImageField(upload_to='shop/products')
    image_4_3_md = models.ImageField(default='', blank=True,
                                     upload_to='shop/products')
    image_4_3_sm = models.ImageField(default='', blank=True,
                                     upload_to='shop/products')
    image_4_3_xs = models.ImageField(default='', blank=True,
                                     upload_to='shop/products')
    date_added = models.DateTimeField(default=timezone.now)
    stock = models.SmallIntegerField(default=0, blank=False, null=False)
    is_unique = models.BooleanField(default=False)
    is_artisanal = models.BooleanField(default=False)
    can_preorder = models.BooleanField(default=False)
    times_purchased = models.IntegerField(
        default=0, blank=False, null=False, editable=False)
    popularity = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        default=0,
        blank=False,
        null=False,
        editable=False)
    slug = models.SlugField(
        default='', editable=False, max_length=254, null=False)

    def get_absolute_url(self):
        """Adds slug to url for page redirection."""
        kwargs = {'slug': self.slug,
                  'pk': self.id
                  }
        return reverse('products:product-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        """Generates default stock values.
        Will restock items that are not unique.
        Updates the 'popularity' value"""
        slug_value_en = self.title_en
        self.slug_en = slugify(slug_value_en, allow_unicode=True)

        slug_value_it = self.title_it
        self.slug_it = slugify(slug_value_it, allow_unicode=True)

        image1, image1_md, image1_sm, image1_xs = responsive_images(
            self, 'image_4_3', 945, 1260, thumb=True)

        if image1:
            self.image_4_3 = image1
            self.image_4_3_md = image1_md
            self.image_4_3_sm = image1_sm
            self.image_4_3_xs = image1_xs

        self.stock = max(self.stock, 0)

        if self.is_unique and self.stock > 1:
            self.stock = 1

        # Updates popularity(See below)
        self._update_popularity()

        super().save(*args, **kwargs)

    def _update_popularity(self):
        """Used for item ordering so more popular items are displayed first.
        A combination of total unique likes and number sold."""
        if self.id:
            self.popularity = self.price / 100 * (
                self.users.count() + self.times_purchased)

    class Meta:
        ordering = ['-popularity']

    def __str__(self):
        return f'{self.title}: €{self.price}'
