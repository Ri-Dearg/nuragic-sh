from django.views.generic import ListView

from .models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 12

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)

        # Selects the active tab
        if 'query' not in self.request.GET and self.request.path == '/shop/':
            all_products_active = True
            context['all_products_active'] = all_products_active

        return context
