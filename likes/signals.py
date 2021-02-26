"""Signal to transfer likes to account on login."""
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in, sender=get_user_model())
def add_unsaved_likes_to_user(
        sender, user, request, **kwargs):  # pylint: disable=unused-argument
    """Transfer and save unauthenticated likes to User account on login."""
    session_likes = request.session.get('likes')
    if session_likes:
        user.userprofile.liked_products.add(*session_likes)
