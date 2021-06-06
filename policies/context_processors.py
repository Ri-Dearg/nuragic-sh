"""Adds site policy documents tp the context."""
from .models import Policy


def get_policies(request):
    """Adds all policies to the context to place them on the footer."""
    all_policies = Policy.objects.filter(display=True).order_by('name')
    active_privacy = Policy.objects.get(active_privacy=True)
    active_cookie = Policy.objects.get(active_cookie=True)
    active_terms = Policy.objects.get(active_terms=True)
    return {'all_policies': all_policies,
            'active_privacy': active_privacy,
            'active_cookie': active_cookie,
            'active_terms': active_terms}
