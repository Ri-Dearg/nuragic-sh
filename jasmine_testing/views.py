"""Views for the Jasmine app."""
from django.http import HttpResponseForbidden
from django.shortcuts import render


# Create your views here.
def run_jasmine(request):
    """Run jasmine tests."""
    if request.user.is_superuser:
        return render(request, 'jasmine_testing/jasmine.html')
    return HttpResponseForbidden()
