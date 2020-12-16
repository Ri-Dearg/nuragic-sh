from django.shortcuts import render
from .models import HomeCarousel, HomeInfo, Review


# Create your views here.
def render_index(request):
    carousel = HomeCarousel.objects.all().filter(display=True)
    info = HomeInfo.objects.all().filter(display=True)
    review = Review.objects.all().filter(display=True)
    context = {'carousel': carousel,
               'info': info,
               'review': review,
               'home_active': True}
    return render(request, 'info/index.html', context)
