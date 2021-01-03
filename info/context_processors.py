"""Adds context to every page."""
from .models import Category


def get_categories(request):
    """Provides category info for the navbar on all pages"""
    categories = Category.objects.all().filter(display=True)
    return {'categories': categories}
