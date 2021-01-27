from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext
from phonenumber_field import widgets

from .models import UserProfile


class StyledLoginForm(LoginForm):
    """Custom styled login form for allauth Signup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs = {'placeholder': _('Password'),
                                                'class': 'form-control'}
        self.fields['remember'].widget.attrs = {
            'class': 'form-check-input'}

        login_widget = forms.TextInput(
            attrs={'placeholder': _('Username or Email'),
                   'class': 'form-control',
                   'autocomplete': 'email'}
        )
        login_field = forms.CharField(
            label=pgettext('label', 'Username or Email'), widget=login_widget
        )
        self.fields['login'] = login_field


class StyledSignupForm(SignupForm):
    """Custom styled signup for allauth Signup."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {'placeholder': _('Email'),
                                             'class': 'form-control'}
        self.fields['username'].widget.attrs = {'placeholder': _('Username'),
                                                'class': 'form-control'}
        self.fields['password1'].widget.attrs = {'placeholder': _('Password'),
                                                 'class': 'form-control'}
        self.fields['password2'].widget.attrs = {
            'placeholder': _('Repeat Password'),
            'class': 'form-control'}


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
