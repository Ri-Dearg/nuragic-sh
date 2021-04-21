import json
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

from products.models import Product

from .models import Order, OrderLineItem


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email on a successful order."""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_email/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_email/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event."""
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe.
        If the payment is processed, the handler will check for the order,
        if it hasn't been made it will create the order.
        Also saves user info to the profile if selected."""

        # Declares variables for use in the view
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info
        user = intent.metadata.user
        userprofile = None
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        # If the user is logged in it re-declares the user variable.
        if user != 'AnonymousUser':
            user = User.objects.get(username=intent.metadata.user)
            userprofile = user.userprofile
            # Saves shipping and billing info if requested by the user.
            if save_info:
                userprofile.shipping_full_name = shipping_details.name
                userprofile.shipping_phone_number = shipping_details.phone
                userprofile.shipping_country = shipping_details.address.country
                userprofile.shipping_postcode = shipping_details.address.postal_code  # noqa E501
                userprofile.shipping_town_or_city = shipping_details.address.city  # noqa E501
                userprofile.shipping_street_address_1 = shipping_details.address.line1  # noqa E501
                userprofile.shipping_street_address_2 = shipping_details.address.line2  # noqa E501
                userprofile.shipping_county = shipping_details.address.state
                userprofile.billing_full_name = billing_details.name
                userprofile.billing_phone_number = billing_details.phone
                userprofile.billing_country = billing_details.address.country
                userprofile.billing_postcode = billing_details.address.postal_code  # noqa E501
                userprofile.billing_town_or_city = billing_details.address.city
                userprofile.billing_street_address_1 = billing_details.address.line1  # noqa E501
                userprofile.billing_street_address_2 = billing_details.address.line2  # noqa E501
                userprofile.billing_county = billing_details.address.state
                userprofile.save()

        # Calculates the correct value for Stripe
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # This checks for the order in the Database
        # and runs a loop to see if it is created in the meantime.
        # If the order is found, it breaks the lopp.
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    email__iexact=billing_details.email,
                    shipping_full_name__iexact=shipping_details.name,
                    shipping_country__iexact=shipping_details.address.country,
                    shipping_postcode__iexact=shipping_details.address.postal_code,         # noqa E501
                    shipping_town_or_city__iexact=shipping_details.address.city,            # noqa E501
                    shipping_street_address_1__iexact=shipping_details.address.line1,  # noqa E501
                    shipping_street_address_2__iexact=shipping_details.address.line2,  # noqa E501
                    shipping_county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        # send an email if the order is found.
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order already in database',
                status=200)
        # If no order is found, it creates the order.
        else:
            order = None
            try:
                order = Order.objects.create(
                    user_profile=userprofile,
                    email=billing_details.email,
                    shipping_full_name=shipping_details.name,
                    shipping_phone_number=shipping_details.phone,
                    shipping_country=shipping_details.address.country,
                    shipping_postcode=shipping_details.address.postal_code,
                    shipping_town_or_city=shipping_details.address.city,
                    shipping_street_address_1=shipping_details.address.line1,
                    shipping_street_address_2=shipping_details.address.line2,
                    shipping_county=shipping_details.address.state,
                    billing_full_name=billing_details.name,
                    billing_phone_number=billing_details.phone,
                    billing_country=billing_details.address.country,
                    billing_postcode=billing_details.address.postal_code,
                    billing_town_or_city=billing_details.address.city,
                    billing_street_address_1=billing_details.address.line1,
                    billing_street_address_2=billing_details.address.line2,
                    billing_county=billing_details.address.state,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(cart).items():
                    try:
                        product = Product.objects.get(id=item_id)
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    except Product.DoesNotExist:
                        order.delete()
                order.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        # Sends a confirmation email after creation
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe."""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
