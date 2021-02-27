"""Views for the PWA app."""
from django.shortcuts import render, reverse
from django.templatetags.static import static
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
            'icon_url': static('favicons/maskable_icon_x512.png'),
            'manifest_url': static('manifest.json'),
            'style_url': static('css/main.css'),
            'home_url': reverse('info:home'),
            'offline_url': reverse('pwa:offline'),
        }
