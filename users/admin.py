"""Registers models to the admin for the Users app."""
from django.contrib import admin

from .models import UserProfile

admin.site.register(UserProfile)
