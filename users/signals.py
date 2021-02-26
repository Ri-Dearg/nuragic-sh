"""Creates UserProfile on User creation"""
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=get_user_model())
def create_or_update_user_profile(
        sender, instance, created, **kwargs):  # NOQA: E501 # pylint: disable=unused-argument
    """Create or update the user profile."""
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
