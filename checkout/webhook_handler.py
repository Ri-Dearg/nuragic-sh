"""Functions that act on receipt of the webhook."""
import json
import logging
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from products.models import Product

from .models import Order, OrderLineItem


def create_order(userprofile, billing_details, shipping_details, cart, pid):
    """Creates the order if it isn't in the DB."""
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
            pass
    order.save()
    complete_order = Order.objects.get(
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
    return complete_order


def check_order_in_db(
        billing_details, shipping_details, grand_total, cart, pid):
    """Runs a loop to check if the order was created in the DB.
    If it was, sends and email, if not, returns False."""
    try:
        order = Order.objects.get(
            email__iexact=billing_details.email,
            shipping_full_name__iexact=shipping_details.name,
            shipping_country__iexact=shipping_details.address.country,
            shipping_town_or_city__iexact=shipping_details.address.city,  # noqa E501
            shipping_street_address_1__iexact=shipping_details.address.line1,  # noqa E501
            grand_total=grand_total,
            original_cart=cart,
            stripe_pid=pid,
        )
    except Order.DoesNotExist:
        order = False
    return order


def save_user_info(userprofile, billing_details, shipping_details):
    """Saves user billing and shipping info to the account."""
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


def send_confirmation_email(order, lang):
    """Send the user a confirmation email on a successful order."""
    translation.activate(lang)

    cust_email = order.email
    subject = render_to_string(
        'checkout/confirmation_email/confirmation_email_subject.txt',
        {'order': order})
    body = render_to_string(
        'checkout/confirmation_email/confirmation_email_body.txt',
        {'order': order,
         'contact_email': 'connect@nuragicshamanichealing.com'})
    body_html = render_to_string(
        'checkout/confirmation_email/confirmation_email_body.html',
        {'order': order,
         'contact_email': 'connect@nuragicshamanichealing.com'})

    send_mail(
        subject,
        body,
        _(f'NuragicSH Order <{settings.DEFAULT_ORDER_EMAIL}>'),
        [cust_email],
        html_message=body_html
    )

    translation.activate('en')
    order_subject = render_to_string(
        'checkout/confirmation_email/order_email_subject.txt',
        {'order': order})
    order_body = render_to_string(
        'checkout/confirmation_email/order_email_body.txt',
        {'order': order, 'contact_email': cust_email})
    order_body_html = render_to_string(
        'checkout/confirmation_email/order_email_body.html',
        {'order': order, 'contact_email': cust_email})

    send_mail(
        order_subject,
        order_body,
        f'NEW ORDER <{settings.DEFAULT_ORDER_EMAIL}>',
        [settings.DEFAULT_ORDER_EMAIL],
        html_message=order_body_html
    )


def invoice_email(intent, grand_total):
    """Sends an email to confirm an invoice is paid."""
    invoice_id = intent.invoice
    order_subject = render_to_string(
        'checkout/confirmation_email/invoice_email_subject.txt',
        {'invoice_id': invoice_id})
    order_body = render_to_string(
        'checkout/confirmation_email/invoice_email_body.txt',
        {'invoice_id': invoice_id, 'amount': grand_total})

    send_mail(
        order_subject,
        order_body,
        f'INVOICE PAID <{settings.DEFAULT_ORDER_EMAIL}>',
        [settings.DEFAULT_ORDER_EMAIL]
    )


def handle_event(event):
    """Handle a generic/unknown/unexpected webhook event."""
    return HttpResponse(
        content=f'Unhandled Webhook received: {event["type"]}',
        status=200)


def handle_payment_intent_payment_failed(event):
    """Handle the payment_intent.payment_failed webhook from Stripe."""
    return HttpResponse(
        content=f'Webhook received: {event["type"]}',
        status=200)


def handle_payment_intent_succeeded(event):
    """Handle the payment_intent.succeeded webhook from Stripe.
    If the payment is processed, the handler will check for the order,
    if it hasn't been made it will create the order.
    Also saves user info to the profile if selected."""

    # Declares variables for use in the view
    intent = event.data.object

    # Calculates the correct value for Stripe
    grand_total = round(intent.charges.data[0].amount / 100, 2)

    if (intent.description) and ('Payment for Invoice' in intent.description):
        invoice_email(intent, grand_total)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Email sent for Invoice.',
            status=200)

    pid = intent.id
    cart = intent.metadata.cart
    lang = intent.metadata.lang
    save_info = intent.metadata.save_info
    user = intent.metadata.user
    userprofile = None
    billing_details = intent.charges.data[0].billing_details
    shipping_details = intent.shipping

    # If the user is logged in it re-declares the user variable.
    if user != 'AnonymousUser':
        user = get_user_model().objects.get(username=intent.metadata.user)
        userprofile = user.userprofile
        # Saves shipping and billing info if requested by the user.
        if save_info:
            save_user_info(userprofile, billing_details, shipping_details)

    # This checks for the order in the Database
    # and runs a loop to see if it is created in the meantime.
    # If the order is found, it breaks the loop.
    attempt = 1
    while attempt <= 6:
        order = check_order_in_db(billing_details, shipping_details,
                                  grand_total, cart, pid)
        if order is False:
            attempt += 1
            time.sleep(1)
        else:
            break

    if order is not False:
        send_confirmation_email(order, lang)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order already in database',
            status=200)
    # If no order is found, it creates the order.
    try:
        order = create_order(userprofile,
                             billing_details,
                             shipping_details,
                             cart,
                             pid)
        # Sends a confirmation email after creation
        send_confirmation_email(order, lang)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Created order in webhook',
            status=200)
    except Exception as error:
        logging.exception(
            'Webhook received: %(type)s | ERROR: %(error)s',
            {'type': event['type'], 'error': error})
        return HttpResponse(status=500)
