from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from useraccount.models import UserAccount
from portfolio_demo import settings

import urllib.request
import ipinfo


def location_data():
    """ returns user location as: (lattitude, longitude) tupple"""

    ipinfo_token = getattr(settings, "IPINFO_TOKEN", None)
    ipinfo_settings = getattr(settings, "IPINFO_SETTINGS", {})
    ip_data = ipinfo.getHandler(ipinfo_token, **ipinfo_settings)

    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    ip_data = ip_data.getDetails(external_ip)

    lat = (ip_data.details['latitude'])
    long = (ip_data.details['longitude'])
    return lat, long


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required. please provide email address")
    address_x = forms.CharField(initial=location_data()[0], widget=forms.HiddenInput())
    address_y = forms.CharField(initial=location_data()[1], widget=forms.HiddenInput())

    class Meta:
        model = UserAccount
        fields = ("email", "username", "password1", "password2", "phone_number", "first_name", "last_name", "address_x",
                  "address_y")


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ("email", "password")

    def clean(self):
        """ validates login_form credentials"""

        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")


class UserAccountUpdateForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ("email", "username", "first_name", "last_name", "phone_number")

    def clean_username(self):
        """ Validates that username is unique """

        if self.is_valid():
            username = self.cleaned_data["username"]
            try:
                account = UserAccount.objects.exclude(pk=self.instance.pk).get(username=username)
            except UserAccount.DoesNotExist:
                return username
            raise forms.ValidationError(f"username {username} is already is use")

    def clean_email(self):
        """ Validates that email is unique """

        if self.is_valid():
            email = self.cleaned_data["email"]
            try:
                account = UserAccount.objects.exclude(pk=self.instance.pk).get(email=email)
            except UserAccount.DoesNotExist:
                return email
            raise forms.ValidationError(f"email {email} is already is use")
