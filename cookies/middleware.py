"""Provides DNT Middleware to track preference."""
from django.utils.cache import patch_vary_headers


class DoNotTrackMiddleware:
    """Provides a Do Not track attribute for request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        """Sets flag request.DNT based on DNT HTTP header.
        Adds a "Vary" header for DNT, useful for caching."""
        patch_vary_headers(response, ['DNT'])
        if 'HTTP_DNT' in request.META and request.META['HTTP_DNT'] == '1':
            request.DNT = True
        else:
            request.DNT = False
        return response
