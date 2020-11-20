from django.urls import path
from .views import run_jasmine

urlpatterns = [
    path('', run_jasmine, name="test"),
]
