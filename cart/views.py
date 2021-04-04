"""Views for cart app: a page for viewing items in the cart
and fetch views to update cart and update the template."""

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from products.models import Product

from .context_processors import get_cart


class CartPageView(TemplateView):  # pylint: disable=too-many-ancestors
    """View that displays all the products in the cart as a list."""
    template_name = 'cart/cart_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = Product.objects.filter(
            stock__gte=1) | Product.objects.filter(
            can_preorder=True).order_by('-stock', '-popularity')

        context['related_products'] = products

        return context


def cart_toggle(request):
    """Add or removes the specified product to the shopping cart.
    The view is Fetch, so it is only called by a JS file.
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

            # Removes items from the cart if it is a once-off unique item or
            # if the remove button is clicked on the cart list page.
            if (item_id in list(cart.keys()) and request.POST.get(
                'special') != 'update') or (
                    request.POST.get('special') == 'remove') or (
                    quantity == 0):
                if item_id in cart:
                    cart.pop(str(item_id))
                    data['message'] = _(
                        f'Removed {product.title} from your cart.')
                else:
                    data['message'] = _(
                        f'Please update the quantity to add \
                            {product.title} to your cart.')

                request.session['cart'] = cart
                data['tag'] = 'info'
                data['tagMessage'] = _('Info')

            # If the other conditions aren't true it is a simple add to cart.
            else:
                if product.is_unique:
                    quantity = 1
                elif (quantity > product.stock
                      and not product.can_preorder):
                    quantity = product.stock

                if (request.POST.get('special') == 'update') and (
                        item_id in cart):
                    # 'update' is sent when product quantity is being changed.
                    data['message'] = f'Updated {product.title} \
                        quantity to {quantity}.'
                elif product.can_preorder and product.stock == 0:
                    data['message'] = _(
                        f'Preordered {quantity} {product.title}.')
                else:
                    data['message'] = _(
                        f'Added {quantity} {product.title} to your cart.')

                cart[item_id] = quantity
                request.session['cart'] = cart

                data['tag'] = 'success'
                data['tagMessage'] = _('Success')

            # Calculates the grand total and
            # then pushes all details into the context.
            RequestContext(request).push(get_cart(request))

            cart_quantity = request.session.get('cart_quantity', 0)
            cart_total = request.session.get('cart_total', '0.00')
            delivery = request.session.get('delivery', '0.00')
            grand_total = request.session.get('grand_total', '0.00')

            request.session['cart_quantity'] = cart_quantity
            request.session['cart_total'] = cart_total
            request.session['delivery'] = delivery
            request.session['grand_total'] = grand_total

            data['result'] = ['cart',
                              cart_quantity,
                              cart_total,
                              delivery,
                              grand_total]

        # If none of the conditions are true, it throws an error.
        except Exception as error:  # pylint: disable=broad-except
            # Calculates the grand total and
            # then pushes all details into the context.
            RequestContext(request).push(get_cart(request))
            data['message'] = _(f'Error adding item to cart: {error}')
            data['result'] = 'error'
            data['tag'] = 'danger'
            data['tagMessage'] = _('Error')

        return JsonResponse(data)
    return HttpResponseForbidden()


def update_cart_offcanvas(request):
    """This view is used to update the cart_popover.html template.
    It is called by the JS file after it successfully receives
    the cart_toggle view response.
    It updates the context using the same logic as the get_cart context
    processor before refreshing the template.
    The JS script then pushes the newly rendered template into
    the popover HTML."""

    # Re-renders the popover template
    return render(request, 'cart/includes/cart_offcanvas.html')
