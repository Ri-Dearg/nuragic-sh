"""Urls for the contact module."""
from django.urls import path

from .views import ProductDetailView, ProductListView, ShopCategoryDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(),
         name='product-detail'),
    path('category/<int:pk>/', ShopCategoryDetailView.as_view(),
         name='shop-category-detail'),
]
