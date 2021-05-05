"""Urls for the policy module."""
from django.urls import path

from .views import PolicyDetailView

urlpatterns = [
    path('policy/<slug:slug>-<int:pk>/', PolicyDetailView.as_view(),
         name='shop-category-detail'),
]
