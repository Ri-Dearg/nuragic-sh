"""Views for the Users app."""
from allauth.account.utils import sync_user_email_addresses
from allauth.account.views import (AddEmailForm, ChangePasswordForm, EmailView,
                                   PasswordChangeView,
                                   sensitive_post_parameters_m)
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import DetailView

from contact.models import Newsletter

from .forms import UserProfileForm


def profile_redirect(request):
    """Redirects to user profile with pk."""
    return redirect('users:user-detail',
                    pk=request.user.id,
                    username=request.user.username)


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    """Renders the user profile only if logged in."""
    user_model = get_user_model()
    model = user_model
    context_object_name = 'user'
    template_name = 'users/user_detail.html'

    def get_context_data(
            self, *args, **kwargs):  # pylint: disable=unused-argument
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)
        user_model = get_user_model()
        # Selects the request user as user id no matter id is put in the url
        user = user_model.objects.get(pk=self.request.user.id)
        profile = user.userprofile
        userprofile_dict = model_to_dict(profile)

        # Adds the forms to the page,
        # setting shipping and billing to saved info.
        add_email_form = AddEmailForm()
        change_password_form = ChangePasswordForm
        user_profile_detail = UserProfileForm(initial=userprofile_dict)

        context['user_profile_detail'] = user_profile_detail
        context['user'] = user
        context['profile'] = profile
        context['add_email_form'] = add_email_form
        context['change_password_form'] = change_password_form
        return context


class CustomEmailView(LoginRequiredMixin, EmailView):
    """Custom email editing view subclassing django-allauth's EMailView
    to maintain use and redirection on the profile page.
    Essentially this is a another DetailView profile page but
    as it is incredibly difficult to have allauth utilise alternative views
    for some functions it was easier to utilise alternative views with
    the same template and context as the basic UserProfile Detailview.
    Apart from the url difference it should be unnoticeable to the user."""
    template_name = 'users/user_detail.html'

    def dispatch(self, request, *args, **kwargs):

        # Retrieves user's emails
        sync_user_email_addresses(request.user)

        # Returns the user to the profile page on success
        self.success_url = reverse_lazy('users:user-detail',
                                        kwargs={
                                            'username': request.user.username,
                                            'pk': request.user.id})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(
            self, *args, **kwargs):  # pylint: disable=unused-argument
        """Adds all necessary information to the context."""
        context = super().get_context_data(**kwargs)
        user_model = get_user_model()
        # Selects the request user as user id no matter id is put in the url
        user = user_model.objects.get(pk=self.request.user.id)
        profile = user.userprofile
        userprofile_dict = model_to_dict(profile)

        # Adds the forms to the page,
        # setting shipping and billing to saved info.
        add_email_form = AddEmailForm()
        change_password_form = ChangePasswordForm
        user_profile_detail = UserProfileForm(initial=userprofile_dict)

        context['user_profile_detail'] = user_profile_detail
        context['user'] = user
        context['profile'] = profile
        context['add_email_form'] = add_email_form
        context['change_password_form'] = change_password_form
        return context


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Custom password editing view subclassing django-allauth's PasswordChangeView
    to maintain use and redirection on the profile page.
    Essentially this is a another DetailView profile page but
    as it is incredibly difficult to have allauth utilise alternative views
    for some functions it was easier to utilise alternative views with
    the same template and context as the basic UserProfile Detailview.
    Apart from the url difference it should be unnoticeable to the user."""

    template_name = 'users/user_detail.html'

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        self.success_url = reverse_lazy('users:user-detail',
                                        kwargs={
                                            'username': request.user.username,
                                            'pk': request.user.id})

        return super().dispatch(
            request, *args, **kwargs)

    def get_context_data(
            self, *args, **kwargs):  # pylint: disable=unused-argument
        """Adds all necessary information to the context"""
        context = super().get_context_data(**kwargs)
        user_model = get_user_model()
        # Selects the request user as user id no matter id is put in the url
        user = user_model.objects.get(pk=self.request.user.id)
        profile = user.userprofile
        userprofile_dict = model_to_dict(profile)

        # Adds the forms to the page,
        # setting shipping and billing to saved info.
        add_email_form = AddEmailForm()
        change_password_form = ChangePasswordForm
        user_profile_detail = UserProfileForm(initial=userprofile_dict)

        context['user_profile_detail'] = user_profile_detail
        context['user'] = user
        context['profile'] = profile
        context['add_email_form'] = add_email_form
        context['change_password_form'] = change_password_form
        return context


@login_required
def update_shipping_billing(request):
    """Updates the user's Shipping and Billing information."""
    # Retrieves the current user and redirection page.
    user = request.user
    userprofile = user.userprofile
    redirect_url = request.GET.get('next', '')
    if request.method == 'POST':
        data = request.POST
        form = UserProfileForm(data=data)
        if form.is_valid():
            # Make sure the correct user is applied to the profile
            # before committing and updating info
            form = UserProfileForm(instance=userprofile, data=data)
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, _('Your information has been updated.'))
            return HttpResponseRedirect(redirect_url)

    form = UserProfileForm()
    messages.warning(request, _('Failed to update your information. \
        Please Check your details.'))
    return HttpResponseRedirect(redirect_url)


@login_required
def update_newsletter(request):
    """Updates the user's Newsletter information."""
    # Retrieves the current user and redirection page.
    redirect_url = request.GET.get('next', '')

    def update_email(email, add_list, remove_list):
        """Updates the newsletter lists"""
        if email in add_list:
            pass
        else:
            add_list.append(email)
            if email in remove_list:
                remove_list.remove(email)

    if request.method == 'POST':
        email = request.POST['email']
        newsletter = Newsletter.objects.filter(
            name='basic').order_by('id').first()
        it_list = newsletter.email_list_it
        en_list = newsletter.email_list_en

        if 'save' in request.POST:
            if 'it' in request.POST['newsletter']:
                update_email(email, it_list, en_list)

            if 'en' in request.POST['newsletter']:
                update_email(email, en_list, it_list)
            newsletter.save()

            messages.success(request, _(
                f'Your newsletter preferences have been updated for {email}.'))
            return HttpResponseRedirect(redirect_url)

        if email in it_list:
            it_list.remove(email)
        if email in en_list:
            en_list.remove(email)
        newsletter.save()

        messages.info(request, _(
            f'You have unsubscribed {email} from the newsletter.'))
        return HttpResponseRedirect(redirect_url)

    messages.warning(request, _(
        'Failed to update your information. Please Check your details.'))
    return HttpResponse(redirect_url)
