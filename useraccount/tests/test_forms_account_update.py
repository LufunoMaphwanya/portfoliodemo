
from useraccount.forms import UserAccountUpdateForm
from django.test import TestCase

from useraccount.models import UserAccount

class TestRegistrationForm(TestCase):
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


    def test_invalid_error_on_update_existing_email(self):
        form = UserAccountUpdateForm()
        assert False is form.is_valid()

        data = {
            "email": "user1@testmail.com",
            "username": "test@gmail.com",
            "password1": "Password56",
            "password2": "Password56",
            "first_name": "Hello",
            "last_name": "Hello",
            "address_x": "-343",
            "phone_number": "0824255626",
            "address_y": "43"
        }
        form = UserAccountUpdateForm(data=data)

        assert True is ('email user1@testmail.com is already is use' in str(form.errors))
        assert False is form.is_valid()

    def test_invalid_error_on_update_existing_username(self):
        form = UserAccountUpdateForm()
        assert False is form.is_valid()

        data = {
            "email": "user122@testmail.com",
            "username": "username1",
            "password1": "Password56",
            "password2": "Password56",
            "first_name": "Hello",
            "last_name": "Hello",
            "address_x": "-343",
            "phone_number": "0824255626",
            "address_y": "43"
        }
        form = UserAccountUpdateForm(data=data)

        assert True is ('username username1 is already is use' in str(form.errors))
        assert False is form.is_valid()

