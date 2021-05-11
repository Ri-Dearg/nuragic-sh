"""Registers models to the admin page."""
from django.contrib import admin

from .models import CookieRecord

admin.site.register(CookieRecord)
