"""Urls for cookie app."""
from django.urls import path

from .views import cookie_consent

urlpatterns = [
    path('consent/', cookie_consent, name='consent'),
]
