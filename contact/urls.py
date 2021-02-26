"""Urls for the contact module."""

from django.urls import path

from .views import CreateEmailView, newsletter_singup

urlpatterns = [
    path('', CreateEmailView.as_view(), name='email-form'),
    path('f/newsletter/', newsletter_singup, name='newsletter'),
]
