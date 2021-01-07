"""Adds context to every page."""
from .models import ShopCategory


def get_shop_categories(request):
    """Provides category info for the navbar on all pages"""
    shop_categories = ShopCategory.objects.all().filter(display=True)
    return {'shop_categories': shop_categories}
