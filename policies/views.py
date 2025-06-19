"""Views for the Policies app."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.views.generic import DetailView

from .models import Policy


class PolicyDetailView(DetailView):
    """Shows the policy on the page."""

    model = Policy


class PolicySitemap(Sitemap):
    """Generate static sitemap URLS.

    Args:
        Sitemap (object): Django Sitemap class.

    """

    changefreq = 'monthly'
    priority = 0.9

    def items(self) -> object:
        """List of view names to include.

        Returns:
            list: List of view names to include.

        """
        return Policy.objects.filter(display=True)

    def lastmod(self, obj: Policy) -> object:
        """Return most recent modification date.

        Args:
            obj (object): The database item.

        Returns:
            object: datetime object.

        """
        return obj.date_created

    def location(self, obj: Policy) -> str:
        """Return urls for the items.

        Args:
            obj (list): The list of view names.

        Returns:
            str: URL for the names.

        """
        return reverse(
            'policies:policy-detail',
            kwargs={'slug': obj.slug, 'pk': obj.pk},
        )
