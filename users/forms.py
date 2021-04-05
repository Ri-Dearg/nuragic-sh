"""Custom allauth forms for custom redirection.
Also includes forms for shipping and billing details."""
from allauth.account.forms import (LoginForm, ResetPasswordForm,
                                   ResetPasswordKeyForm, SignupForm)
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Column, Field, Fieldset, Layout,
                                 MultiWidgetField, Row)
from django import forms
from django.utils.translation import pgettext
from django.utils.translation import ugettext_lazy as _
from phonenumber_field import widgets

from .models import UserProfile


class StyledLoginForm(LoginForm):
    """Custom styled login form for allauth Signup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        login_field = forms.CharField(
            label=pgettext('label', 'Username or E-mail'))
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
                      autocomplete='email', css_class='p-font text-primary'),

                Field('password', placeholder=_('Password'),
                      css_class='p-font text-primary'),

                HTML(f'<a class="p-font smooth-click text-white \
                     text-center mt-1 mb-2 secondaryAction" \
                     href="{account_reset}">\
                {forgot_password}</a>'),

                Field('remember'),

                Column(
                    StrictButton(
                        _('Sign In'),
                        type='submit',
                        css_class='p-font btn-tran btn btn-warning text-primary \
                            shadow primaryAction'),
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
                      autocomplete='email', css_class='p-font text-primary',
                      pattern=r'^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'),  # noqa E501 # pylint: disable=line-too-long
                Column(StrictButton(_('Reset Password'), type='submit',
                                    css_class='p-font btn-tran btn btn-warning \
                                    text-primary shadow'),
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
                Field('password1',
                      placeholder=_('New Password'),
                      autocomplete='off', minlength='8',
                      css_class='p-font text-primary'),

                Field('password2',
                      placeholder=_('Repeat Password'),
                      autocomplete='off', minlength='8',
                      css_class='p-font text-primary'),

                Column(StrictButton(_('Change Password'), type='submit',
                                    css_class='p-font btn-tran btn btn-warning \
                           text-primary shadow'),
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
                Field('email', placeholder=_('E-mail'),
                      css_class='p-font text-primary',
                pattern=r'^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'),  # noqa E501 # pylint: disable=line-too-long

                Field('username',  placeholder=_('Username'),
                      css_class='p-font text-primary'),

                Field('password1', placeholder=_('Password'),
                      minlength='8', css_class='p-font text-primary'),

                Field('password2', placeholder=_('Repeat Password'),
                      minlength='8', css_class='p-font text-primary'),

                Column(StrictButton(_('Register'), type='submit',
                                    css_class='p-font btn-tran btn btn-warning \
                                    text-primary shadow'),
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
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        helper = self.helper
        helper.form_action = 'users:shipping-billing'
        helper.form_id = 'shipping_billing_form'
        helper.form_tag = False

        self.fields['shipping_phone_number'] = forms.CharField(
            widget=widgets.PhoneNumberPrefixWidget(),
            required=False)

        self.fields['billing_phone_number'] = forms.CharField(
            widget=widgets.PhoneNumberPrefixWidget(),
            required=False)

        self.fields['shipping_full_name'].label = _('Full Name')
        self.fields['shipping_street_address_1'].label = _('Street Address 1')
        self.fields['shipping_street_address_2'].label = _('Street Address 2')
        self.fields['shipping_town_or_city'].label = _('Town or City')
        self.fields['shipping_county'].label = _('County, State or Locality')
        self.fields['shipping_country'].label = _('Country')

        self.fields['billing_full_name'].label = _('Full Name')
        self.fields['billing_street_address_1'].label = _('Street Address 1')
        self.fields['billing_street_address_2'].label = _('Street Address 2')
        self.fields['billing_town_or_city'].label = _('Town or City')
        self.fields['billing_county'].label = _('County, State or Locality')
        self.fields['billing_postcode'].label = _('Postcode')
        self.fields['billing_country'].label = _('Country')

        helper.layout = Layout(
            Row(
                Column(
                    Fieldset(_('SHIPPING DETAILS'),
                             Row(
                        Field('shipping_full_name',
                              placeholder=_('Full Name'),
                              css_class='p-font text-primary'),
                        MultiWidgetField(
                            'shipping_phone_number',
                            template='bootstrap4/phone_field.html'
                        ),
                        Field('shipping_street_address_1',
                              placeholder=_('Street Address 1'),
                              css_class='p-font text-primary'),
                        Field('shipping_street_address_2',
                              placeholder=_('Street Address 2'),
                              css_class='p-font text-primary'),
                        Field('shipping_town_or_city',
                              placeholder=_('Town or City'),
                              css_class='p-font text-primary'),
                        Field('shipping_county',
                              placeholder=_('County, State or Locality'),
                              css_class='p-font text-primary'),
                        Field('shipping_postcode',
                              placeholder=_('Postcode'),
                              css_class='p-font text-primary'),
                        Field('shipping_country',
                              placeholder=_('Country'),
                              css_class='form-select p-font text-primary')
                    )),
                    css_class='col-12 col-md-6 p-2 px-md-4 pt-md-4 pb-md-2'),

                Column(
                    Fieldset(_('BILLING DETAILS'),
                             Row(
                        Field('billing_full_name',
                              placeholder=_('Full Name'),
                              css_class='p-font text-primary'),
                        MultiWidgetField(
                            'billing_phone_number',
                            template='bootstrap4/phone_field.html'
                        ),
                        Field('billing_street_address_1',
                              placeholder=_('Street Address 1'),
                              css_class='p-font text-primary'),
                        Field('billing_street_address_2',
                              placeholder=_('Street Address 2'),
                              css_class='p-font text-primary'),
                        Field('billing_town_or_city',
                              placeholder=_('Town or City'),
                              css_class='p-font text-primary'),
                        Field('billing_county',
                              placeholder=_('County, State or Locality'),
                              css_class='p-font text-primary'),
                        Field('billing_postcode',
                              placeholder=_('Postcode'),
                              css_class='p-font text-primary'),
                        Field('billing_country',
                              placeholder=_('Country'),
                              css_class='form-select p-font text-primary')
                    )),
                    css_class='col-12 col-md-6 p-2 px-md-4 pt-md-4 pb-md-2'),

                Column(StrictButton(_('Save Details'), type='submit',
                                    css_class='p-font btn-tran btn btn-sm \
                                        btn-warning text-primary shadow'),
                       css_class='col-12 col-md-auto ps-2 pb-2 px-md-4 \
                           pb-md-4 mx-md-auto')
            )
        )
