"""Adds site policy documents tp the context."""
from .models import Policy


def get_policies(request):
    """Adds all policies to the context to place them on the footer."""
    all_policies = Policy.objects.all().filter(display=True).order_by('name')
    return {'all_policies': all_policies}
