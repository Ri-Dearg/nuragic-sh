from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin

from .models import Product, ShopCategory


class ShopCategoryDetailView(DetailView, MultipleObjectMixin):
    model = ShopCategory
    paginate_by = 4

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        object_list = self.object.products.all().order_by(
            '-stock', '-popularity')
        context = super(ShopCategoryDetailView, self).get_context_data(
            object_list=object_list, **kwargs)

        return context


class ProductListView(ListView):
    model = Product
    paginate_by = 4

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)

        # Selects the active tab
        if 'query' not in self.request.GET and self.request.path == '/shop/':
            all_products_active = True
            context['all_products_active'] = all_products_active

        return context
