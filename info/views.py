"""Views for the info app."""

from django.contrib.sitemaps import Sitemap
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from .models import Category, Page, Review, SplashImage


# Create your views here.
def render_index(request):
    """Renders the index with context for categories and splash images."""
    carousel = SplashImage.objects.filter(
        info_display=True
    ) & SplashImage.objects.exclude(page__isnull=True, product__isnull=True)
    review = Review.objects.filter(display=True)
    context = {'carousel': carousel, 'review': review, 'home_active': True}
    return render(request, 'info/index.html', context)


class CategoryDetailView(DetailView):
    """Renders the category detail page."""

    model = Category

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)

        this_object = context['object']
        # Selects the active tab
        if f'{this_object.slug}-{this_object.id}' in self.request.path:
            context['active_category'] = f'{this_object.id}'
            context['active_all'] = f'{this_object.id}'

        return context


class PageDetailView(DetailView):
    """Renders the category detail page."""

    model = Page

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)

        this_object = context['object']
        # Selects the active tab
        if f'{this_object.slug}-{this_object.id}' in self.request.path:
            category_id = this_object.category.id
            context['active_category'] = f'{category_id}'
            context['active_page'] = f'{this_object.id}'

        return context


class InfoSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        categories = Category.objects.filter(display=True)
        pages = Page.objects.filter(display=True)
        return list(categories) + list(pages)

    def lastmod(self, obj):
        return obj.date_added

    def location(self, obj):
        if isinstance(obj, Category):
            return reverse(
                'info:category-detail', kwargs={'slug': obj.slug, 'pk': obj.pk}
            )
        if isinstance(obj, Page):
            return reverse(
                'info:page-detail', kwargs={'slug': obj.slug, 'pk': obj.pk}
            )
        return reverse(obj)
