"""Urls for cart app."""
from django.urls import path

from .views import CartListView, cart_toggle, refresh_total, update_cart

urlpatterns = [
    path('', CartListView.as_view(), name='cart-list'),
    path('ajax/toggle/', cart_toggle, name='cart-toggle'),
    path('update/', update_cart, name='cart-update'),
    path('totals/', refresh_total, name='cart-refresh'),
]
