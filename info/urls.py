"""Urls for the info module"""

from django.urls import path
from .views import render_index, CategoryDetailView

urlpatterns = [
    path('', render_index, name="home"),
    path('category/<int:pk>/',
         CategoryDetailView.as_view(), name='category-detail'),
]
