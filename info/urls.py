"""Urls for the info module."""

from django.urls import path

from .views import CategoryDetailView, PageDetailView, render_index

urlpatterns = [
    path('', render_index, name="home"),
    path('category/<slug:slug>-<int:pk>/',
         CategoryDetailView.as_view(), name='category-detail'),
    path('article/<int:pk>/',
         PageDetailView.as_view(), name='page-detail'),
]
