"""Views for the info app."""
from django.shortcuts import render
from django.views.generic import DetailView

from .models import Category, Page, Review, SplashImage


# Create your views here.
def render_index(request):
    """Renders the index with context for categories and splash images."""
    carousel = SplashImage.objects.filter(
        info_display=True) & SplashImage.objects.exclude(
            page__isnull=True, product__isnull=True)
    review = Review.objects.filter(display=True)
    context = {'carousel': carousel,
               'review': review,
               'home_active': True}
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
