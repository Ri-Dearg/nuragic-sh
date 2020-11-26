from django.shortcuts import render
from .models import HomeCarousel


# Create your views here.
def render_index(request):
    carousel = HomeCarousel.objects.all()
    return render(request, 'info/index.html', {'carousel': carousel})
