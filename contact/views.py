"""Views for the Contact app."""
import json
import urllib

from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Hidden, Layout, Row
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import reverse
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from info.models import Category

from .models import Email, Newsletter


class CreateEmailView(SuccessMessageMixin, CreateView):
    """The page used for contact to send an email."""
    model = Email
    context_object_name = 'email'
    fields = ['email', 'name', 'subject', 'message']
    success_message = _('Thank you, your message has been sent.')

    def get_form(self, form_class=None):
        """Adds custom placeholders and widgets to form."""
        form = super().get_form(form_class)
        form.fields['email'].label = _('Email')
        form.fields['name'].label = _('Name')
        form.fields['subject'].label = _('Subject')
        form.fields['message'].label = _('What are your thoughts?')

        form.helper = FormHelper(form)
        helper = form.helper
        helper.form_action = 'contact:email-form'
        helper.form_class = 'rounded p-2'
        helper.form_id = 'contact-form'
        helper.floating_labels = True
        helper.use_custom_control = False

        helper.layout = Layout(
            Row(
                Field('email',  placeholder=_('Email'),
                      pattern=r'^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$',  # noqa E501  # pylint: disable=line-too-long
                      wrapper_class='col-md-6',
                      css_class='p-font text-primary'),

                Field('name', placeholder=_('Name'),
                      wrapper_class='col-md-6',
                      css_class='p-font text-primary'),

                Field('subject', placeholder=_('Subject'),
                      css_class='p-font text-primary'),

                Field('message',
                      placeholder=_('What are your thoughts?'),
                      css_class='p-font text-primary'),

                HTML(
                    '<div class="g-recaptcha" data-callback="captchaCallback" \
                        data-size="compact" \
                        data-sitekey="6Lc1BT0bAAAAAM3StPLPHk9zrg1_rO-7TMU62STK">\
                            </div>'),

                Hidden('recaptcha',
                       f'{reverse("contact:recaptcha")}', id="recap-url"),

                Column(StrictButton(_('Send'),
                       disabled='disabled',
                       css_class='pixel-contact p-font btn-tran btn-warning text-primary shadow fw-bold',  # noqa E501
                       css_id='contact-submit'),
                       css_class='col-12 my-1 text-center'),
                )
        )

        return form

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context.
        Highlights the 'Contact' in the navbar."""
        context = super().get_context_data(**kwargs)
        # Details necessary for Stripe payment processing
        this_object = Category.objects.get(title_en__iexact='about')
        context['active_category'] = f'{this_object.id}'

        return context


@csrf_exempt
def recaptcha_verify(request):
    """Verifies the recaptcha."""
    if request.method == 'POST':
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_SECRET,
            'response': request.POST.get('g-recaptcha-response'),
            'remoteip': request.META['REMOTE_ADDR']
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        data = {}
        data['result'] = 'error'
        data['message'] = _('Captcha verification failed, please try again.')
        if result['success']:
            data['result'] = 'success'
        return JsonResponse(data)
    return HttpResponseForbidden()


def newsletter_singup(request):
    """Inserts email into newsletter list.
    Runs through selected language and adds them
    to the appropriate mailing list. Is an ajax view."""
    if request.method == 'POST':
        data = {}
        newsletter = Newsletter.objects.filter(
            name='basic').order_by('id').first()
        if get_language() == 'it':
            email_list = newsletter.email_list_it
        if get_language() == 'en':
            email_list = newsletter.email_list_en
        if request.POST[f'email_{get_language()}'] in email_list:
            data['message'] = _(
                'You have already signed up for the newsletter.')
            data['tag'] = 'info'
            data['tagMessage'] = _('Info')

            return JsonResponse(data)

        email_list.append(request.POST[f'email_{get_language()}'])
        newsletter.save()
        data['message'] = _('Thank you for signing up!')
        data['tag'] = 'success'
        data['tagMessage'] = _('Success')
        return JsonResponse(data)
    return HttpResponse(status=403)
