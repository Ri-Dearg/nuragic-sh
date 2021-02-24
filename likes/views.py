"""Views for like app: a page for viewing likes
and fetch views to update likes and update the template."""
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from products.models import Product


class LikesListView(ListView):  # pylint: disable=too-many-ancestors
    """View that displays all the liked products for the user."""
    model = Product
    template_name = 'likes/likes_list.html'

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context.
        Gets likes from the account if the user is logged in,
        else it creates a list from the session to display the likes.
        Sorts the list in reverse chronological if the user is logged in.
        Finally it paginates for infinite scroll."""

        context = super().get_context_data(**kwargs)

        # Sets initial variables for the context
        user = self.request.user
        context['products'] = []

        # Adds liked products from the account if logged in.
        if user.is_authenticated:
            liked_products = user.userprofile.liked_products.order_by(
                '-liked__datetime_added')
            for product in liked_products:
                context['products'].append(product)

        # Otherwise it creates a list of IDs and retrieves the products from
        # the DB before adding them to the context.
        else:
            id_list = []
            session_likes = self.request.session.get('likes')

            if session_likes:
                for key in session_likes:
                    id_list.append(key)
                liked_products = Product.objects.filter(id__in=id_list)

                for product in liked_products:
                    context['products'].append(product)

        # Paginates the items.
        products = context['products']
        paginator = Paginator(products, 6)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


def likes_toggle(request):
    """Add or removes the specified product to likes.
    The view is Ajax, so it is only called by a JS file.
    It checks whether the user is authenticated or anonymous and
    runs different functions accordingly.
    The decorator converts the response to JSON format.
    It is then picked up by the JS file which completes the page effects.
    'tag' and 'message' are used to display the toasts.
    'result' is used to define the logic on the JS side."""

    data = {}
    if request.method == 'POST':
        # Runs through a number of variables to process the ajax call.
        # If it fails, it throws an exception with a message.
        try:
            item_id = request.POST.get('item-id')
            product = get_object_or_404(Product, pk=item_id)

            # Saves the item to the profile if the user is logged in, otherwise
            # saves to the session
            if request.user.is_authenticated:
                # Retrieves the User's liked products
                user = request.user
                liked_products = user.userprofile.liked_products

                # If the product is in the list it is unliked,
                # otherwise it is liked.
                if product in liked_products.all():
                    user.userprofile.liked_products.remove(product)
                    product.save()
                    data['message'] = _(
                        f'{product.title} removed from bookmarks.')
                    data['result'] = 'unliked'
                    data['tag'] = 'info'
                    data['tagMessage'] = _('Info')
                else:
                    user.userprofile.liked_products.add(product)
                    product.save()
                    data['message'] = _(f'{product.title} bookmarked!')
                    data['result'] = 'liked'
                    data['tag'] = 'success'
                    data['tagMessage'] = _('Success')

            # If the user is anonymous the items get added to the session.
            else:
                likes = request.session.get('likes', [])

                # If the product is in the list it is unliked,
                # otherwise it is liked.
                if item_id in likes:
                    likes.remove(item_id)
                    request.session['likes'] = likes
                    data['message'] = _(
                        f'{product.title} removed from bookmarks.')
                    data['result'] = 'unliked'
                    data['tag'] = 'info'
                    data['tagMessage'] = _('Info')
                else:
                    likes.append(item_id)
                    request.session['likes'] = likes
                    data['message'] = _(f'{product.title} bookmarked!')
                    data['result'] = 'liked'
                    data['tag'] = 'success'
                    data['tagMessage'] = _('Success')

        # If none of the conditions are true, it throws an error.
        except Exception as error:  # pylint: disable=broad-except
            data['message'] = _(f'Error liking item: %r, {error}')
            data['result'] = 'error'
            data['tag'] = 'error'
            data['tagMessage'] = _('Error')

        return JsonResponse(data)
    return HttpResponseForbidden


def update_likes(request):
    """This view is used to update the likes_popover.html template.
    It is called by the JS file after it successfully receives
    the likes_toggle view response.
    It updates the context using the same logic as the get_likes context
    processor before refreshing the template.
    The JS script then pushes the newly rendered template into
    the popover HTML."""

    # Initializes a list for use with the context
    likes = []

    # Saves the item to the profile if the user is logged in, otherwise
    # saves to the session
    user = request.user
    if user.is_authenticated:
        liked_products = user.userprofile.liked_products.order_by(
            '-liked__datetime_added')
        for product in liked_products:
            likes.append(product)

    # Creates a list of IDs and retrieves the products from
    # the DB before adding them to the context.
    else:
        id_list = []
        session_likes = request.session.get('likes')

        if session_likes:
            for key in session_likes:
                id_list.append(key)
            liked_products = Product.objects.filter(id__in=id_list)

            for product in liked_products:
                likes.append(product)

    # Pushes the new context to the page before re-rendering the template.
    RequestContext(request).push({'likes': likes})
    return render(request, 'likes/includes/likes_dropdown.html')
