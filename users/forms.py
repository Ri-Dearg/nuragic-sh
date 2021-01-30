from allauth.account.forms import (LoginForm, ResetPasswordForm,
                                   ResetPasswordKeyForm, SignupForm)
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext
from phonenumber_field import widgets

from .models import UserProfile


class StyledLoginForm(LoginForm):
    """Custom styled login form for allauth Signup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        login_field = forms.CharField(
            label=pgettext('label', 'Username or Email'))
        self.fields['login'] = login_field

        self.helper = FormHelper(self)
        helper = self.helper
        helper.form_action = 'account_login'
        helper.form_class = 'login rounded p-2'
        helper.field_class = 'col-md-6'

        account_reset = '{% url "account_reset_password" %}'
        forgot_password = _('Forgot Password?')

        helper.layout = Layout(
            HTML('{% if redirect_field_value %}<input type="hidden" \
                name="{{ redirect_field_name }}" \
                value="{{ redirect_field_value }}" />{% endif %}'),

            Row(
                Field('login', placeholder=_('Username or E-mail'),
                      autocomplete='email'),

                Field('password', placeholder=_('Password')),

                HTML(f'<a class="p-font smooth-click text-white \
                     text-center mt-1 mb-2 secondaryAction" \
                     href="{account_reset}">\
                {forgot_password}</a>'),

                Field('remember'),

                Column(StrictButton(_('Sign In'), type='submit',
                             css_class='p-font btn-tran btn btn-warning text-primary shadow primaryAction'),  # noqa E501
                       css_class='col-auto mx-auto'),
            )
        )


class StyledResetPasswordForm(ResetPasswordForm):
    """Custom styled rest password form for allauth Signup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        helper = self.helper
        helper.form_action = 'account_reset_password'
        helper.form_class = 'password_reset rounded p-2'

        helper.layout = Layout(
            HTML('{% if redirect_field_value %}<input type="hidden" \
                name="{{ redirect_field_name }}" \
                value="{{ redirect_field_value }}" />{% endif %}'),

            Row(
                Field('email', placeholder=_('E-mail'),
                      autocomplete='email'),

                Column(StrictButton(_('Reset Password'), type='submit',
                             css_class='p-font btn-tran btn btn-warning text-primary shadow'),  # noqa E501
                       css_class='col-auto mt-1 mx-auto'),
            )
        )


class StyledResetPasswordKeyForm(ResetPasswordKeyForm):
    """Custom styled rest password form for allauth Signup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        helper = self.helper
        helper.field_class = 'col-md-6'
        helper.form_tag = False

        helper.layout = Layout(
            HTML('{% if redirect_field_value %}<input type="hidden" \
                name="{{ redirect_field_name }}" \
                value="{{ redirect_field_value }}" />{% endif %}'),

            Row(
                Field('password1', placeholder=_('New Password'),
                      autocomplete='off', minlength='8'),

                Field('password2', placeholder=_('Repeat Password'),
                      autocomplete='off', minlength='8'),

                Column(StrictButton(_('Change Password'), type='submit',
                       css_class='p-font btn-tran btn btn-warning text-primary shadow'),  # noqa E501
                       css_class='col-auto mt-1 mx-auto'),
            )
        )


class StyledSignupForm(SignupForm):
    """Custom styled signup for allauth Signup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        helper = self.helper
        helper.form_action = 'account_signup'
        helper.form_id = 'signup_form'
        helper.form_class = 'singup rounded p-2'
        helper.field_class = 'col-md-6'

        helper.layout = Layout(
            HTML('{% if redirect_field_value %}<input type="hidden" \
                name="{{ redirect_field_name }}" \
                value="{{ redirect_field_value }}" />{% endif %}'),

            Row(
                Field('email',  placeholder=_('E-mail'),
                pattern='^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'),  # noqa E501

                Field('username',  placeholder=_('Username')),

                Field('password1', placeholder=_('Password'),
                      minlength='8'),

                Field('password2', placeholder=_('Repeat Password'),
                      minlength='8'),

                Column(StrictButton(_('Register'), type='submit',
                             css_class='p-font btn-tran btn btn-warning text-primary shadow'),  # noqa E501
                       css_class='col-auto mx-auto mt-1'),
            )
        )


class UserProfileForm(forms.ModelForm):
    """Allows for the updating of the user's billing/shipping info."""
    class Meta:
        model = UserProfile
        fields = ['billing_full_name', 'billing_phone_number',
                  'billing_street_address_1', 'billing_street_address_2',
                  'billing_town_or_city', 'billing_county',
                  'billing_country', 'billing_postcode', 'shipping_full_name',
                  'shipping_phone_number', 'shipping_street_address_1',
                  'shipping_street_address_2', 'shipping_town_or_city',
                  'shipping_county', 'shipping_country', 'shipping_postcode']

    def __init__(self, *args, **kwargs):
        """Selects custom layout and placeholders for the form."""
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        helper = self.helper
        helper.form_action = 'users:shipping-billing'
        helper.form_id = 'shipping_billing_form'
        self.fields['shipping_full_name'].widget.attrs = {'placeholder': 'Full Name'}  # noqa E501
        self.fields['shipping_full_name'].label = 'Full Name'
        self.fields['shipping_phone_number'] = forms.CharField(
            widget=widgets.PhoneNumberPrefixWidget(
                attrs={
                    'type': 'tel',
                    'placeholder': 'Phone Number',
                    'class': 'form-control',
                    'pattern': '[0-9]+',
                }),
            required=False)
        self.fields['shipping_street_address_1'].widget.attrs = {
            'placeholder': '123 Main St.'}
        self.fields['shipping_street_address_1'].label = 'Street Address 1'
        self.fields['shipping_street_address_2'].widget.attrs = {
            'placeholder': 'Street Address 2'}
        self.fields['shipping_street_address_2'].label = 'Street Address 2'
        self.fields['shipping_town_or_city'].widget.attrs = {
            'placeholder': 'Town or City'}
        self.fields['shipping_town_or_city'].label = 'City or Town'
        self.fields['shipping_county'].widget.attrs = {
            'placeholder': 'Locality'}
        self.fields['shipping_county'].label = 'County, State or Locality'
        self.fields['shipping_country'].widget.attrs = {'placeholder': 'Country',  # noqa E501
                                                        'class': 'form-control'}  # noqa E501
        self.fields['shipping_country'].label = 'Country'
        self.fields['shipping_postcode'].widget.attrs = {
            'placeholder': 'Postcode'}
        self.fields['shipping_postcode'].label = 'Postcode'
        self.fields['billing_full_name'].widget.attrs = {
            'placeholder': 'Full Name', 'class': 'billing-field'}
        self.fields['billing_full_name'].label = 'Full Name'
        self.fields['billing_phone_number'] = forms.CharField(
            label='Phone Number',
            widget=widgets.PhoneNumberPrefixWidget(
                attrs={
                    'type': 'tel',
                    'placeholder': 'Phone Number',
                    'class': 'form-control billing-field',
                    'pattern': '[0-9]+',
                }),
            required=False)
        self.fields['billing_street_address_1'].widget.attrs = {
            'Placeholder': 'Street Address 1', 'class': 'billing-field'}
        self.fields['billing_street_address_1'].label = 'Street Address 1'
        self.fields['billing_street_address_2'].widget.attrs = {
            'placeholder': 'Street Address 2'}
        self.fields['billing_street_address_2'].label = 'Street Address 2'
        self.fields['billing_town_or_city'].widget.attrs = {
            'placeholder': 'Town or City', 'class': 'billing-field'}
        self.fields['billing_town_or_city'].label = 'City or Town'
        self.fields['billing_county'].widget.attrs = {
            'placeholder': 'Locality'}
        self.fields['billing_county'].label = 'County, State or Locality'
        self.fields['billing_country'].widget.attrs = {'placeholder': 'Country',  # noqa E501
                                                       'class': 'form-control billing-field'}  # noqa E501
        self.fields['billing_country'].label = 'Country'
        self.fields['billing_postcode'].widget.attrs = {
            'placeholder': 'Postcode'}
        self.fields['billing_postcode'].label = 'Postcode'