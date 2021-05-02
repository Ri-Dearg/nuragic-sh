"""Urls for like app."""
from django.urls import path

from .views import LikesListView, likes_toggle, update_likes_offcanvas

urlpatterns = [
    path('your-likes/', LikesListView.as_view(), name='likes-list'),
    path('ajax/toggle/', likes_toggle, name='likes-toggle'),
    path('update_offcanvas/', update_likes_offcanvas, name='likes-offcanvas'),
]
