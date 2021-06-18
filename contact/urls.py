"""Urls for the contact module."""

from django.urls import path

from .views import CreateEmailView, newsletter_singup, recaptcha_verify

urlpatterns = [
    path('', CreateEmailView.as_view(), name='email-form'),
    path('f/recaptcha/', recaptcha_verify, name='recaptcha'),
    path('f/newsletter/', newsletter_singup, name='newsletter'),
]
