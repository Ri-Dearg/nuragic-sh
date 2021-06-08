"""Urls for cookie app."""
from django.urls import path

from .views import cookie_consent, update_cookies

urlpatterns = [
    path('consent/', cookie_consent, name='consent'),
    path('update/', update_cookies, name='update'),
]
