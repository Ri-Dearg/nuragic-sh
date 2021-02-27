"""Views for the PWA app."""
from django.shortcuts import render
from django.views.generic import TemplateView

from config import version


def render_offline(request):
    """Renders a page explaining the app is offline."""
    return render(request, 'pwa/offline.html')


class SWTemplateView(TemplateView):
    """Prepares he Service Worker for the PWA."""
    template_name = 'pwa/serviceworker.js'
    content_type = 'application/javascript'

    def get_context_data(self, **kwargs):
        return {
            'version': version,
        }
