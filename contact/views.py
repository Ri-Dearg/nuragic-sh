from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse

from .models import Email, Newsletter


class CreateEmailView(SuccessMessageMixin, CreateView):
    """The page used for contatc to send an email."""
    model = Email
    context_object_name = 'email'
    fields = ['email', 'name', 'subject', 'message']
    success_message = 'Thank you, your message has been sent.'

    def get_form(self, form_class=None):
        """Adds custom placeholders and widgets to form."""
        form = super().get_form(form_class)
        form.fields['email'].widget.attrs = {'placeholder': 'Email Address'}
        form.fields['name'].widget.attrs = {'placeholder': 'Full Name'}
        form.fields['subject'].widget.attrs = {'placeholder': 'The Topic'}
        form.fields['message'].widget.attrs = {
            'placeholder': 'What are your thoughts?*'}
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
        if request.POST['email'] in newsletter.email_list:
            data["message"] = "You have already signed up for the newsletter."
            data["tag"] = "info"
            return JsonResponse(data)

        newsletter.email_list.append(request.POST['email'])
        newsletter.save()
        data["message"] = "Thank you for signing up!"
        data["tag"] = "success"
        return JsonResponse(data)
    return HttpResponse(status=500)
