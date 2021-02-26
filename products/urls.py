"""Urls for the contact module."""
from django.urls import path

from .views import ProductListView, ShopCategoryDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('category/<int:pk>/', ShopCategoryDetailView.as_view(),
         name='shop-category-detail'),
]
