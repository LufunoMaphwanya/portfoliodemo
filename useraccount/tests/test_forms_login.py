from useraccount.forms import LoginForm
from django.test import TestCase

from useraccount.models import UserAccount


class TestLoginForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        for i in range(0, 10):
            UserAccount.objects.create(
                email=f"user{i}@testmail.com",
                username=f"username{i}",
                first_name=f"person-{i}",
                last_name=f"person-{i}",
                phone_number=f"surname-{i}",
                address_x=f"400",
                address_y=f"-200",
            )

    def test_valid_login_form(self):
        form = LoginForm()
        assert False is form.is_valid()
