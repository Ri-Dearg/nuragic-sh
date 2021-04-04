"""Urls for cart app."""
from django.urls import path

from .views import CartPageView, cart_toggle, update_cart_offcanvas

urlpatterns = [
    path('cart_list/', CartPageView.as_view(), name='cart-list'),
    path('ajax/toggle/', cart_toggle, name='cart-toggle'),
    path('update_offcanvas/', update_cart_offcanvas, name='cart-offcanvas'),
]
