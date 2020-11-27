from django.shortcuts import render
from .models import HomeCarousel, HomeInfo


# Create your views here.
def render_index(request):
    carousel = HomeCarousel.objects.all().filter(display=True)
    info = HomeInfo.objects.all().filter(display=True)
    context = {'carousel': carousel,
               'info': info}
    return render(request, 'info/index.html', context)
