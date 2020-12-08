from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.http import HttpResponse, JsonResponse

from .models import Email, Newsletter


class CreateEmailView(SuccessMessageMixin, CreateView):
    """The page used for contatc to send an email."""
    model = Email
    context_object_name = 'email'
    fields = ['email', 'name', 'subject', 'message']
    success_message = _('Thank you, your message has been sent.')

    def get_form(self, form_class=None):
        """Adds custom placeholders and widgets to form."""
        form = super().get_form(form_class)
        form.fields['email'].widget.attrs = {'placeholder': 'Email*',
                                             'class': 'form-control'}
        form.fields['email'].label = 'Email*'
        form.fields['name'].widget.attrs = {'placeholder': 'Name*',
                                            'class': 'form-control'}
        form.fields['name'].label = 'Name*'
        form.fields['subject'].widget.attrs = {'placeholder': 'Subject*',
                                               'class': 'form-control'}
        form.fields['subject'].label = 'Subject*'
        form.fields['message'].widget.attrs = {
            'placeholder': 'What are your thoughts?*',
            'class': 'form-control'}
        form.fields['message'].label = ''
        return form

    def get_context_data(self, **kwargs):
        """Adds all necessary information to the context.
        Mainly just highlights the "Contact" in the navbar."""
        context = super().get_context_data(**kwargs)
        # Details necessary for Stripe payment processing
        contact_active = True

        context['contact_active'] = contact_active
        return context


def newsletter_singup(request):
    """Inserts email into newsletter list."""
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
