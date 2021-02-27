"""Urls for the info module."""

from django.urls import path

from .views import CategoryDetailView, PageDetailView, render_index

urlpatterns = [
    path('', render_index, name='home'),
    path('category/<int:pk>/',
         CategoryDetailView.as_view(), name='category-detail'),
    path('page/<int:pk>/',
         PageDetailView.as_view(), name='page-detail'),
]
