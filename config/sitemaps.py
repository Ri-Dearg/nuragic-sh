from info.views import InfoSitemap
from policies.views import PolicySitemap

from .views import StaticSitemap

sitemaps = {
    'static': StaticSitemap,
    'info': InfoSitemap,
    'policy': PolicySitemap,
}
