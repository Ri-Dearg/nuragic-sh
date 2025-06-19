"""Views for the Policies app."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.views.generic import DetailView

from .models import Policy


class PolicyDetailView(DetailView):
    """Shows the policy on the page."""

    model = Policy


class PolicySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Policy.objects.filter(display=True)

    def lastmod(self, obj):
        return obj.date_created

    def location(self, obj):
        return reverse(
            'policies:policy-detail',
            kwargs={'slug': obj.slug, 'pk': obj.pk},
        )
