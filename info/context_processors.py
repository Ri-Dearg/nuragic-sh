"""Adds context to every page."""
from products.models import ShopCategory

from .models import Category


def get_categories(request):
    """Provides category info for the navbar on all pages."""
    if 'shop' in request.path:
        shop_categories = ShopCategory.objects.all().filter(display=True)
        return {'categories': shop_categories}

    categories = Category.objects.all().filter(display=True)
    return {'categories': categories}
