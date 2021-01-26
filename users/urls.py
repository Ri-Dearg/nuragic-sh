from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (UserProfileDetailView,
                    CustomEmailView,
                    CustomPasswordChangeView,
                    update_shipping_billing)

urlpatterns = [
    path('profile/<int:pk>/', login_required(UserProfileDetailView.as_view()),
         name='user-detail'),
    path('accounts/email/', login_required(CustomEmailView.as_view()),
         name='user-email'),
    path('accounts/password/change/',
         login_required(CustomPasswordChangeView.as_view()),
         name='user-change-password'),
    path('shipping-billing/',
         login_required(update_shipping_billing),
         name='shipping-billing'),
]
