"""Custom adapter for allauth page redirection."""
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import HttpResponseRedirect


class CustomAdapter(DefaultAccountAdapter):
    """An adapter subclassed from django-allauth
    to utilise the "next" query request for redirection."""

    def respond_email_verification_sent(self, request, user):
        next_page = request.GET.get('next', '')
        return HttpResponseRedirect(next_page)
