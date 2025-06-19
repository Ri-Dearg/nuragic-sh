from info.views import InfoSitemap
from policies.views import PolicySitemap
from products.views import ShopSitemap

from .views import StaticSitemap

sitemaps = {
    'static': StaticSitemap,
    'info': InfoSitemap,
    'policy': PolicySitemap,
    'shop': ShopSitemap,
}
