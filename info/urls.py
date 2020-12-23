"""Urls for the info module"""

from django.urls import path

from .views import CategoryDetailView, DetailInfoDetailView, render_index

urlpatterns = [
    path('', render_index, name="home"),
    path('category/<int:pk>/',
         CategoryDetailView.as_view(), name='category-detail'),
    path('detailinfo/<int:pk>/',
         DetailInfoDetailView.as_view(), name='detailinfo-detail'),
]
