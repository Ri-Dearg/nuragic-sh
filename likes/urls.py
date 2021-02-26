"""Urls for like app."""
from django.urls import path

from .views import LikesListView, likes_toggle, update_likes

urlpatterns = [
    path('', LikesListView.as_view(), name='likes-list'),
    path('ajax/toggle/', likes_toggle, name='likes-toggle'),
    path('update/', update_likes, name='likes-update'),
]
