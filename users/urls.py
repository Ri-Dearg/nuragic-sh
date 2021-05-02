"""Urls for the users module."""
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (CustomEmailView, CustomPasswordChangeView,
                    UserProfileDetailView, profile_redirect, update_newsletter,
                    update_shipping_billing)

urlpatterns = [
    path('profile/', login_required(profile_redirect),
         name='user-redirect'),
    path(
        'your-profile/<str:username>-<int:pk>/', login_required(
            UserProfileDetailView.as_view()),
        name='user-detail'),
    path('c/email/', login_required(CustomEmailView.as_view()),
         name='user-email'),
    path('c/password/change/',
         login_required(CustomPasswordChangeView.as_view()),
         name='user-change-password'),
    path('shipping-billing/',
         login_required(update_shipping_billing),
         name='shipping-billing'),
    path('newsletter/',
         login_required(update_newsletter),
         name='newsletter'),
]
