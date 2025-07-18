"""Url Patterns for the Checkout App."""

from django.urls import path

from .views import OrderCreateView, OrderDetailView, OrderListView, cache_data
from .webhooks import webhook

checkout_urlpatterns = [
    path('payment/', OrderCreateView.as_view(), name='order-create'),
    path(
        'your-order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'
    ),
    path('your-orders/', OrderListView.as_view(), name='order-list'),
]

webhook_urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path('cache_data/', cache_data, name='cache-data'),

]
