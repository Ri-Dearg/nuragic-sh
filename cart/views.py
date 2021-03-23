"""Views for cart app: a page for viewing items in the cart
and fetch views to update cart and update the template."""
from decimal import Decimal

from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from config import settings
from products.models import Product


class CartListView(ListView):  # pylint: disable=too-many-ancestors
    """View that displays all the products in the cart as a list."""
    model = Product
    context_object_name = 'products'
    template_name = 'cart/cart_list.html'


def cart_toggle(request):
    """Add or removes the specified product to the shopping cart.
    The view is Ajaxed, so it is only called by a JS file.
    It runs through numerous variables such as item stock,
    whether the item is unique, etc, before giving a response.
    The decorator converts the response to JSON format.
    It is then picked up by the JS file which completes the page effects.
    'tag' and 'message' are used to display the toasts.
    'result' and 'special' are used to define the logic on the JS side."""

    data = {}
    if request.method == "POST":
        # Runs through a number of variables to process the ajax call.
        # If it fails, it throws an exception with a message.
        try:
            # Tries to retrieve the item and quantity,
            # if no item was given it is set to '0' to throw an error.
            item_id = request.POST.get('item-id', '0')
            product = get_object_or_404(Product, pk=item_id)
            quantity = int(request.POST.get('quantity'))

            # Gets the cart to run through item details.
            cart = request.session.get('cart', {})

            # 'update' is sent when product quantity is being changed.
            # Despite the 'uncart' result variable it doesn't uncart but
            # actually updates quantity on the cart list page.
            # if request.POST.get('special') == 'update':
            #   cart[item_id] = quantity

            #    # Checks stock and if the quantity requestd is greater,
            #    # it sets it to the max available.
            #    if cart[item_id] > product.stock:
            #         cart[item_id] = product.stock
            #     request.session['cart'] = cart

            #     # Defines the variables to be sent the JS file.
            #     tag = 'success'
            #     message = f'Updated {product.name} quantity to \
            #         {cart[item_id]}.'
            #     result = 'uncarted'

            # Removes items from the cart if it is a once-off unique item or
            # if the remove button is clicked on the cart list page.
            if (item_id in list(cart.keys())) or (
                    request.POST.get('special') == 'remove'):
                cart.pop(str(item_id))

                request.session['cart'] = cart
                data['message'] = _(f'Removed {product.title} from your cart.')
                data['result'] = 'uncarted'
                data['tag'] = 'info'
                data['tagMessage'] = _('Info')

            # If the other conditions aren't true it is a simple add to cart.
            else:
                cart[item_id] = quantity
                if cart[item_id] > product.stock:
                    cart[item_id] = product.stock

                request.session['cart'] = cart
                data['message'] = _(f'Added {product.title} to your cart.')
                data['result'] = 'carted'
                data['tag'] = 'success'
                data['tagMessage'] = _('Success')

        # If none of the conditions are true, it throws an error.
        except Exception as error:  # pylint: disable=broad-except
            data['message'] = _(f'Error: %r, {error}')
            data['result'] = 'error'
            data['tag'] = 'danger'
            data['tagMessage'] = _('Error')

        # If there is a special case in the POST data,
        # it gets passed to the JS file for its logic.
        # Else, it sends the variables declare in the 'if' clauses.
        if 'special' in request.POST:
            data['special'] = request.POST.get('special')
            return JsonResponse(data)
        return JsonResponse(data)
    return HttpResponseForbidden()


def update_cart(request):
    """This view is used to update the cart_popover.html template.
    It is called by the JS file after it successfully recieves
    the cart_toggle view response.
    It updates the context using the same logic as the get_cart context
    processor before refreshing the template.
    The JS script then pushes the newly rendered template into
    the popover HTML."""

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
                                 'A Product is unavailable.')

            # If the product is valid and in stock,
            # it calculates details for that item:
            if product is not False:
                if product.stock >= 1:
                    cart_total += item_data * product.price
                    cart_items.append({
                        'item_id': item_id,
                        'quantity': item_data,
                        'product': product})

                # Or else the item is removed from the cart with feedback:
                else:
                    cart.pop(item_id)
                    messages.warning(request,
                                     f'{product} has run out of stock!')

            # Skips the product if it is not False:
            else:
                pass

    # Checks the cart total price and declares delivery price accordingly.
    # The FREE_DELIVERY_THRESHOLD is a set price declared in settings.
    if cart_total < settings.FREE_DELIVERY_THRESHOLD and cart_total > 0:
        delivery = Decimal(settings.STANDARD_DELIVERY)
    else:
        delivery = 0

    grand_total = cart_total + delivery
    request.session.save()

    # Calculates the grand total and then pushes all details into the context.
    RequestContext(request).push({'cart': cart,
                                  'cart_quantity': cart_quantity,
                                  'cart_items': cart_items,
                                  'cart_total': cart_total,
                                  'delivery': delivery,
                                  'grand_total': grand_total})

    # Re-renders the popover template
    return render(request, 'cart/includes/cart_popover.html')


def refresh_total(request):
    """One the cart list page, this refreshes the totals box template.
    Other context info is handled by the update_crt view."""

    return render(request, 'cart/includes/totals.html')
