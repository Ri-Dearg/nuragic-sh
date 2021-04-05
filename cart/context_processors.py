"""Adds carted items to the context."""
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from products.models import Product


def get_cart(request):
    """Creates a cart context in the session and adds it to all pages.
    Checks details like quantity, stock, total cost as well as whether an item
    is invalid or not."""

    # Declares variables for use with the cart.
    cart = request.session.get('cart')
    cart_items = []
    cart_total = 0
    cart_quantity = 0

    if cart:
        # Creates a copy of the cart dictionary for iteration:
        temp_cart = cart.copy()
        for item_id, item_data in temp_cart.items():
            # Sets the total quantity of an item:
            cart_quantity += item_data
            # Confirms the item is valid or throws an error with a message:
            try:
                product = Product.objects.get(pk=item_id)
            except Product.DoesNotExist:
                # Declares product as false and removes it:
                product = False
                cart.pop(item_id)
                messages.warning(request,
                                 _('A Product is unavailable.'))

            # If the product is valid and in stock,
            # it calculates details for that item:
            if product is not False:
                if product.stock >= 1 or product.can_preorder:
                    cart_total += item_data * product.price
                    cart_items.append({
                        'item_id': item_id,
                        'quantity': item_data,
                        'product': product})

                # Or else the item is removed from the cart with feedback:
                else:
                    cart.pop(item_id)
                    messages.warning(
                        request,
                        _(f'{product} has run out of stock \
                            and has been removed from the cart.'))

            # Skips the product if it is False:
            else:
                pass

        request.session['cart'] = cart

    # Checks the cart total price and declares delivery price accordingly.
    # The FREE_DELIVERY_THRESHOLD is a set price declared in settings.
    # if cart_total < settings.FREE_DELIVERY_THRESHOLD and cart_total > 0:
    delivery = Decimal(settings.STANDARD_DELIVERY)
    # else:
    # delivery = 0

    # Calculates the grand total and then pushes all details into the context.
    grand_total = cart_total + delivery
    request.session['cart_quantity'] = cart_quantity
    request.session['cart_total'] = str(cart_total)
    request.session['grand_total'] = str(grand_total)
    request.session['delivery'] = "{:.2f}".format(delivery)

    request.session.save()
    return {'cart': cart,
            'cart_quantity': cart_quantity,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'delivery': delivery,
            'grand_total': grand_total}
