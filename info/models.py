"""Models for the info module."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from tinymce.models import HTMLField

from products.models import Product

from .utils import responsive_images


class SplashImage(models.Model):
    """Allows for the creation of a collection of carousel items.
    You can add a splash image which will be resized and a blurb.
    Images are different sizes depending on the screen size.
    I would recommend cropping your images first."""
    # pylint: disable=too-many-instance-attributes

    page = models.OneToOneField('Page',
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL)
    product = models.OneToOneField(Product,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL)
    title = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=200, default='')
    image_tw_header = models.ImageField(upload_to='info/carousel')
    image_tw_header_md = models.ImageField(
        upload_to='info/carousel', default='', blank=True)
    image_tw_header_sm = models.ImageField(
        upload_to='info/carousel', default='', blank=True)
    image_fb_link = models.ImageField(
        upload_to='info/carousel')
    image_fb_link_md = models.ImageField(
        upload_to='info/carousel', default='', blank=True)
    image_fb_link_sm = models.ImageField(
        upload_to='info/carousel', default='', blank=True)
    info_display = models.BooleanField(default=True)
    shop_display = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Resizes and saves images.
        Selects either Page or Product as field."""

        if self.page:
            self.product = None
        elif self.product:
            self.page = None

        image1, image1_md, image1_sm = responsive_images(
            self, 'image_tw_header', 1260, 420)

        image2, image2_md, image2_sm = responsive_images(
            self, 'image_fb_link', 1200, 630)

        if image1:
            self.image_tw_header = image1
            self.image_tw_header_md = image1_md
            self.image_tw_header_sm = image1_sm
        if image2:
            self.image_fb_link = image2
            self.image_fb_link_md = image2_md
            self.image_fb_link_sm = image2_sm

        super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['-date_added']

    def __str__(self):
        link = None
        if self.page:
            link = self.page
        if self.product:
            link = self.product
        return f'{link}: {self.title}'


class Category(models.Model):
    """Allows for the creation of a collection of Products.
    You can add a splash image which will be resized and a blurb.
    Images will be resized on upload to 1200x630px shape.
    I would recommend cropping your images first."""
    title = models.CharField(max_length=30, null=False)
    menu_word = models.CharField(max_length=10, null=False)
    description = HTMLField()
    button_text = models.CharField(max_length=30, null=False)
    image_fb_link = models.ImageField(upload_to='info/category')
    image_fb_link_md = models.ImageField(
        upload_to='info/category', default='', blank=True)
    image_fb_link_sm = models.ImageField(
        upload_to='info/category', default='', blank=True)
    display = models.BooleanField(default=True)
    order = models.SmallIntegerField(validators=[MaxValueValidator(12),
                                                 MinValueValidator(0)])
    date_added = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(
        default='', editable=False, max_length=30, null=False)

    def get_absolute_url(self):
        """Adds slug to url for page redirection."""
        kwargs = {'slug': self.slug,
                  'pk': self.id}
        return reverse('products:product-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        """Creates and adds url slug.
        Resizes and saves images."""
        slug_value = _(self.title)
        self.slug = slugify(slug_value, allow_unicode=True)

        image1, image1_md, image1_sm = responsive_images(
            self, 'image_fb_link', 1200, 630)
        if image1:
            self.image_fb_link = image1
            self.image_fb_link_md = image1_md
            self.image_fb_link_sm = image1_sm
        super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['order']
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.menu_word}'


class Page(models.Model):  # pylint: disable=too-many-instance-attributes
    """Detailed pages for Categories"""
    theme_choices = [('secondary', 'beige'),
                     ('info', 'blue'),
                     ('brown', 'brown'),
                     ('success', 'green'),
                     ('primary', 'navy'),
                     ('purple', 'purple'),
                     ('danger', 'red'),
                     ('warning', 'yellow'), ]

    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        related_name='page')
    product = models.ForeignKey(Product,
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL,
                                related_name='page')
    product_button_text = models.CharField(
        max_length=30, blank=True, default=_('Learn More'))
    title = models.CharField(max_length=60, null=False)
    summary = models.CharField(max_length=400, null=False)
    button_text = models.CharField(
        max_length=30, null=False, default=_('Learn More'))
    desc_title1 = models.CharField(max_length=60, null=False)
    description1 = HTMLField()
    desc_title2 = models.CharField(max_length=60, blank=True, default='')
    description2 = HTMLField(blank=True, default='')
    title_image_tw_header = models.ImageField(upload_to='info/page/title')
    title_image_tw_header_md = models.ImageField(
        upload_to='info/page/title', default='', blank=True)
    title_image_tw_header_sm = models.ImageField(
        upload_to='info/page/title', default='', blank=True)
    image_fb_link = models.ImageField(
        upload_to='info/page/desc')
    image_fb_link_md = models.ImageField(
        upload_to='info/page/desc', default='', blank=True)
    image_fb_link_sm = models.ImageField(
        upload_to='info/page/desc', default='', blank=True)
    bot_image_tw_header = models.ImageField(
        upload_to='info/page/bot', blank=True, default='')
    bot_image_tw_header_md = models.ImageField(
        upload_to='info/page/bot', blank=True, default='')
    bot_image_tw_header_sm = models.ImageField(
        upload_to='info/page/bot', blank=True, default='')
    order = models.SmallIntegerField(validators=[MaxValueValidator(12),
                                                 MinValueValidator(0)])
    theme = models.CharField(
        max_length=10, choices=theme_choices, default='info')
    date_added = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(
        default='', editable=False, max_length=60, null=False)

    def get_absolute_url(self):
        """Adds slug to url for page redirection."""
        kwargs = {'slug': self.slug,
                  'pk': self.id
                  }
        return reverse('info:page-detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        """Creates and adds url slug.
        Resizes and saves images."""
        slug_value = _(self.title)
        self.slug = slugify(slug_value, allow_unicode=True)

        image1, image1_md, image1_sm = responsive_images(
            self, 'title_image_tw_header', 1260, 420)
        image2, image2_md, image2_sm = responsive_images(
            self, 'image_fb_link', 1200, 630)
        image3, image3_md, image3_sm = responsive_images(
            self, 'bot_image_tw_header', 1260, 420)

        if image1:
            self.title_image_tw_header = image1
            self.title_image_tw_header_md = image1_md
            self.title_image_tw_header_sm = image1_sm

        if image2:
            self.image_fb_link = image2
            self.image_fb_link_md = image2_md
            self.image_fb_link_sm = image2_sm

        if image3:
            self.bot_image_tw_header = image3
            self.bot_image_tw_header_md = image3_md
            self.bot_image_tw_header_sm = image3_sm

        super().save(*args, **kwargs)

    class Meta:
        """Orders by the most recent created by default."""
        ordering = ['order']

    def __str__(self):
        return f'{self.category}: {self.title}'


class Review(models.Model):
    """Allows for the creation of reviews."""
    reviewer_name = models.CharField(max_length=50, null=False)
    text = models.TextField()
    display = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.reviewer_name}'
