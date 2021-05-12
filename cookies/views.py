"""Saves cookie consent details in the session and creates cookie records."""
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.translation import ugettext_lazy as _

from .models import CookieRecord


def cookie_consent(request):
    """Saves Cookie consent details and creates a record."""
    data = {}
    user = None
    if request.method == 'POST':
        request.session['cookie_consent'] = False
        consent = request.POST['cookie-consent']
        if consent == 'opt-in':
            request.session['cookie_consent'] = True

        if request.user.is_authenticated:
            user = request.user

        CookieRecord(user=user,
                     ip_address=request.META['REMOTE_ADDR'],
                     consent=request.session['cookie_consent']
                     ).save()

        data['message'] = _('Cookie preferences saved.')
        data['tag'] = 'info'
        data['tagMessage'] = _('Info')
        return JsonResponse(data)
    return HttpResponseForbidden()
