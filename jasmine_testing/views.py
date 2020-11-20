from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def run_jasmine(request):
    if request.user.is_superuser:
        return render(request, 'jasmine_testing/jasmine.html')
    else:
        return HttpResponse(status=500)
