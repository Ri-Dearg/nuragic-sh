"""Urls to access jasmine app."""
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import run_jasmine

urlpatterns = [
    path('', login_required(run_jasmine), name="test"),
]
