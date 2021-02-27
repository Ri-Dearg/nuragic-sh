"""Views for the PWA app."""
from django.views.generic import TemplateView

from config import version


class SWTemplateView(TemplateView):
    """Prepares he Service Worker for the PWA."""
    template_name = 'pwa/serviceworker.js'
    content_type = 'application/javascript'

    def get_context_data(self, **kwargs):
        return {
            'version': version,
        }
