"""Views for the Policies app."""
from django.views.generic import DetailView
from .models import Policy


class PolicyDetailView(DetailView):
    """Shows the policy on the page."""
    model = Policy
