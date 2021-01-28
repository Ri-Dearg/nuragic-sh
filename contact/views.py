"""Views for the Contact app."""
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
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
        helper.label_class = 'p-font text-primary sr-only'
        helper.field_class = 'col-12 form-floating my-1'
        helper.floating_labels = True

        helper.layout = Layout(
            Row(
                Column(Field('email',  placeholder=_('Email'),
                pattern='^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'),  # noqa E501
                        css_class=f'{helper.field_class} col-md-6'),

                Column(Field('name', placeholder=_('Name')),
                       css_class=f'{helper.field_class} col-md-6'),

                Column(Field('subject', placeholder=_('Subject')),
                       css_class=f'{helper.field_class}'),

                Column(Field('message',
                       placeholder=_('What are your thoughts?')),
                       css_class=f'{helper.field_class}'),

                Column(StrictButton(_('Send'), type='submit',
                             css_class="p-font btn-tran btn-warning text-primary shadow"),  # noqa E501
                       css_class='col-12 my-1 text-center'),
                css_class='row')
        )

        return form

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context.
        Mainly just highlights the "Contact" in the navbar."""
        context = super().get_context_data(**kwargs)
        # Details necessary for Stripe payment processing
        this_object = Category.objects.get(title_en__iexact='about')
        context['active_category'] = f'{this_object.id}'

        return context


def newsletter_singup(request):
    """Inserts email into newsletter list.
    Runs through selected language and adds them
    to the appropriate mailing list"""
    if request.method == "POST":
        data = {}
        newsletter = Newsletter.objects.get(name='basic')
        if get_language() == 'it':
            email_list = newsletter.email_list_it
        if get_language() == 'en':
            email_list = newsletter.email_list_en
        if request.POST[f'email_{get_language()}'] in email_list:
            data["message"] = _(
                "You have already signed up for the newsletter.")
            data["tag"] = "info"
            data["tagMessage"] = _('Info')

            return JsonResponse(data)

        email_list.append(request.POST[f'email_{get_language()}'])
        newsletter.save()
        data["message"] = _("Thank you for signing up!")
        data["tag"] = "success"
        data["tagMessage"] = _('Success')
        return JsonResponse(data)
    return HttpResponse(status=403)
