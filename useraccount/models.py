from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, phone_number=None, first_name=None, last_name=None, address_x=None, address_y=None):
        if not email:
            raise ValueError("User must have email address")
        if not username:
            raise ValueError("User must have username")

        user = self.model(
            email = self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError("User must have email address")
        if not username:
            raise ValueError("User must have username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class UserAccount(AbstractBaseUser):
    """
        Stores a single user-account
        extends :model:`django.contrib.auth.models.AbstractBaseUser`
    """
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField( max_length=30, unique=True)
    date_joined = models.DateTimeField( verbose_name="date joined", auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)

    address_x = models.CharField(max_length=100)
    address_y = models.CharField(max_length=100)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    objects = MyAccountManager()

    def __str__(self):
        """returns user email to represent user account as str."""
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True