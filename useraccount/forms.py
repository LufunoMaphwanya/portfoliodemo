from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from useraccount.models import UserAccount

from portfolio_demo import settings
import urllib.request
import ipinfo

def location_data():
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
    address_y = forms.CharField(initial=location_data()[1],  widget=forms.HiddenInput())

    class Meta:
        model = UserAccount
        fields = ("email", "username", "password1", "password2", "phone_number", "first_name", "last_name", "address_x", "address_y")


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ("email", "password")

    def clean(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")