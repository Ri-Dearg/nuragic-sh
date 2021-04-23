import uuid

from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from products.models import Product
from users.models import CustomPhoneNumberField, UserProfile


class Order(models.Model):
    """Model that sets the fields for orders.
    The majority of fields are required.
    The user-profile field is optional but will be set for logged in users."""

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')
    email = models.EmailField(max_length=254, null=False, blank=False)

    shipping_full_name = models.CharField(
        max_length=50, null=False, blank=False)
    shipping_phone_number = CustomPhoneNumberField(null=False, blank=False)
    shipping_street_address_1 = models.CharField(
        max_length=80, null=False, blank=False)
    shipping_street_address_2 = models.CharField(
        max_length=80, default='', blank=True)
    shipping_town_or_city = models.CharField(
        max_length=40, null=False, blank=False)
    shipping_county = models.CharField(max_length=80, blank=True)
    shipping_postcode = models.CharField(max_length=20, default='', blank=True)
    shipping_country = CountryField(
        blank_label=_('Country'), null=False, blank=False)

    billing_full_name = models.CharField(
        max_length=50, null=False, blank=False)
    billing_phone_number = CustomPhoneNumberField(null=False, blank=False)
    billing_street_address_1 = models.CharField(
        max_length=80, null=False, blank=False)
    billing_street_address_2 = models.CharField(
        max_length=80, default='', blank=True)
    billing_town_or_city = models.CharField(
        max_length=40, null=False, blank=False)
    billing_county = models.CharField(max_length=80, default='', blank=True)
    billing_postcode = models.CharField(max_length=20, default='', blank=True)
    billing_country = CountryField(
        blank_label=_('Country'), null=False, blank=False)

    date = models.DateTimeField(auto_now_add=True, editable=False)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False)
    stripe_pid = models.CharField(max_length=254,
                                  null=False, blank=False)

    def get_absolute_url(self):
        """Redirects users to their order once it has been created."""
        return reverse('checkout:order-detail', args=[str(self.id)])

    def _update_total(self):
        """Updates the grand total figure in an order."""
        self.order_total = self.lineitems.aggregate(Sum(
            'lineitem_total'))['lineitem_total__sum'] or 0
        self.grand_total = self.order_total + self.delivery_cost

    def _generate_order_number(self):
        """Generates a random order number."""
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """Saves the order number and updates the total."""
        self._update_total()
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """Associates the product to the order with quantity and total cost.
    All fields are required."""

    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              null=False, blank=False,
                              related_name='lineitems')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         editable=False,
                                         null=False, blank=False)

    def save(self, *args, **kwargs):
        """Calculates the total cost and saves the details.
        Also removes stock."""
        self.lineitem_total = self.product.price * self.quantity
        self.product.stock = self.product.stock - self.quantity
        self.product.times_purchased += self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.title} on order {self.order.order_number}'
