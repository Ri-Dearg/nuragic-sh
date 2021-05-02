"""Url Patterns for the Checkout App."""
from django.urls import path

from .views import OrderCreateView, OrderDetailView, OrderListView, cache_data
from .webhooks import webhook

urlpatterns = [
    path('payment/', OrderCreateView.as_view(), name='order-create'),
    path('your-order/<int:pk>/',
         OrderDetailView.as_view(), name='order-detail'),
    path('your-orders/',
         OrderListView.as_view(), name='order-list'),
    path('cache_data/', cache_data, name='cache-data'),
    path('webhook/', webhook, name='webhook'),
]
