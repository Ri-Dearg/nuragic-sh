"""Views for the Jasmine app."""
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def run_jasmine(request):
    """Run jasmine tests."""
    if request.user.is_superuser:
        return render(request, 'jasmine_testing/jasmine.html')
    else:
        return HttpResponse(status=500)
