from .views import StaticSitemap
from info.views import InfoSitemap

sitemaps = {
    'static': StaticSitemap,
    'info': InfoSitemap,
}
