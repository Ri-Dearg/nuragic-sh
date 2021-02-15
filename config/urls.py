"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Patterns for the shop section functions
shop_patterns = [
    path('', include(('products.urls', 'products'),
                     namespace='products')),
    path('likes/', include(('likes.urls', 'likes'),
                           namespace='likes'))
]

urlpatterns = [
    # Internationalization functions
    path('i18n/', include('django.conf.urls.i18n')),
    # Allauth functions
    path('accounts/', include('allauth.urls')),
    # Rich Text Editor functions
    path('tinymce/', include('tinymce.urls')),
    # Jasmine testing functions
    path('jasmine/', include(('jasmine_testing.urls', 'jasmine_testing'),
                             namespace='jasmine')),
    path('contact/', include(('contact.urls', 'contact'),
                             namespace='contact')),
    path('', include(('info.urls', 'info'),
                     namespace='info')),
    path('shop/', include(shop_patterns)),
    path('users/', include(('users.urls', 'users'),
                           namespace='users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)
