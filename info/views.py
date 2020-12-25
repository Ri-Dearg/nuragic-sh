from django.shortcuts import render
from django.views.generic import DetailView

from .models import Category, DetailInfo, HomeCarousel, Review


# Create your views here.
def render_index(request):
    carousel = HomeCarousel.objects.all().filter(display=True)
    review = Review.objects.all().filter(display=True)
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
        if f'/category/{this_object.id}' in self.request.path:
            context['active_category'] = f'{this_object.id}'
            context['active_all'] = f'{this_object.id}'

        return context


class DetailInfoDetailView(DetailView):
    """Renders the category detail page."""
    model = DetailInfo

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)

        this_object = context['object']
        # Selects the active tab
        if f'/detailinfo/{this_object.id}' in self.request.path:
            category_id = this_object.category.id
            context['active_category'] = f'{category_id}'
            context['active_page'] = f'{this_object.id}'

        return context
