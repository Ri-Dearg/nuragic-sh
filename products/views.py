"""Views for the Products app."""
from django.views.generic import DetailView, ListView
from django.views.generic.list import MultipleObjectMixin

from info.models import SplashImage

from .models import Product, ShopCategory


class ShopCategoryDetailView(DetailView, MultipleObjectMixin):
    """Displays a list of products in the Category.
    The MultipleObjectMixin allows for easy pagination."""
    model = ShopCategory
    paginate_by = 12

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        # Declares objects for pagination
        object_list = self.object.products.filter(
            stock__gte=1) | self.object.products.filter(
            can_preorder=True).order_by('-stock', '-popularity')
        context = super().get_context_data(
            object_list=object_list, **kwargs)

        this_object = context['object']
        # Selects the active tab
        if f'{this_object.slug}-{this_object.id}' in self.request.path:
            context['active_category'] = f'{this_object.id}'

        return context


class ProductDetailView(DetailView):
    """Displays details for a product."""
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        this_object = context['product']

        product_category = this_object.category

        # Renders related products from the same category
        # while removing the current product.
        products = Product.objects.exclude(
            pk=this_object.id).filter(
                category=product_category, stock__gte=1
        ) | Product.objects.exclude(
            pk=this_object.id).filter(
            category=product_category, can_preorder=True
        ).order_by('-stock', '-popularity').order_by(
            '-stock', '-popularity')[:9]

        context['related_products'] = products

        # Selects the active tab
        context['active_category'] = f'{product_category.id}'

        return context


class ProductListView(ListView):  # pylint: disable=too-many-ancestors
    """Displays all products in a list.
    Adds context for highlighting the menu."""
    queryset = Product.objects.filter(
        stock__gte=1) | Product.objects.filter(
        can_preorder=True).order_by('-stock', '-popularity')
    paginate_by = 12

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)
        # Selects the active tab
        if 'query' not in self.request.GET and self.request.path == '/shop/':
            # Adds Carousel info
            carousel = SplashImage.objects.filter(
                shop_display=True) & SplashImage.objects.exclude(
                page__isnull=True, product__isnull=True)
            context['carousel'] = carousel

            all_products_active = True
            context['all_products_active'] = all_products_active

        return context
