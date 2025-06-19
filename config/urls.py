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
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from . import views as config_views

# Sitemap generator classes.
sitemaps = {
    'static': config_views.StaticSitemap,
}

# Handlers for custom error pages
handler404 = 'config.views.custom_page_not_found'
handler403 = 'config.views.custom_permission_denied'
handler400 = 'config.views.custom_bad_request'
handler500 = 'config.views.custom_server_error'

# Patterns for the shop section functions
shop_patterns = [
    path('', include(('products.urls', 'products'), namespace='products')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path(
        'checkout/',
        include(('checkout.urls', 'checkout'), namespace='checkout'),
    ),
    path('likes/', include(('likes.urls', 'likes'), namespace='likes')),
]

account_patterns = [
    # Allauth functions
    path('', include('allauth.urls')),
    path('', include(('users.urls', 'users'), namespace='users')),
]

urlpatterns = [
    # Internationalization functions
    path('i18n/', include('django.conf.urls.i18n')),
    # Rich Text Editor functions
    path('tinymce/', include('tinymce.urls')),
    # Jasmine testing functions
    path(
        'jasmine/',
        include(
            ('jasmine_testing.urls', 'jasmine_testing'), namespace='jasmine'
        ),
    ),
    # My apps
    path('robots.txt', config_views.serve_robots_txt, name='robots'),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps, 'content_type': 'application/xml'},
        name='django.contrib.sitemaps.views.sitemap',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include(account_patterns)),
    path(
        'contact-us/',
        include(('contact.urls', 'contact'), namespace='contact'),
    ),
    path('cookies/', include(('cookies.urls', 'cookie'), namespace='cookies')),
    path('', include(('info.urls', 'info'), namespace='info')),
    path(
        'policies/',
        include(('policies.urls', 'policies'), namespace='policies'),
    ),
    path('shop/', include(shop_patterns)),
)
