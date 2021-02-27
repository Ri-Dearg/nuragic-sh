"""Urls for the pwa module."""
from django.urls import path

from .views import SWTemplateView

urlpatterns = [
    # Service Worker Template string
    path(
        'sw.js',
        SWTemplateView.as_view(),
        name='service-worker',
    ),
]
