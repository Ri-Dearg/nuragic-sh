"""Adds context from settings file."""
from django.conf import settings


def global_settings(request):
    """Imports version number into the context.
    This is used to refresh JS and CSS static files."""
    return {
        'VERSION': settings.VERSION,
    }
