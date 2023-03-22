from useraccount.forms import RegistrationForm
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

    def test_valid_registration_form(self):
        form = RegistrationForm()
        assert False is form.is_valid()

        data = {
            "email": "test@gmail.com",
            "username": "test@gmail.com",
            "password1": "Password56",
            "password2": "Password56",
            "first_name": "Hello",
            "last_name": "Hello",
            "address_x": "-343",
            "phone_number": "0824255626",
            "address_y": "43"
        }

        assert True is RegistrationForm(data=data).is_valid()

    def test_invalid_registration_form(self):
        form = RegistrationForm()
        assert False is form.is_valid()

        invalid_registrations = [
            {
                "email": "test@gmail.com",
                "username": "test@gmail.com",
                "password1": "Testing123",
                "password2": "Testing1234",  # passwords do not match
                "first_name": "Hello",
                "last_name": "Hello",
                "address_x": "-343",
                "address_y": "43"
            },
            {
                "password1": "Password56",
                "password2": "Password56",
                "first_name": "Hello",
                "last_name": "Hello",  # no email/username provided
                "address_x": "-343",
                "address_y": "43"
            }
        ]

        assert False is RegistrationForm(data=invalid_registrations[0]).is_valid()
        assert False is RegistrationForm(data=invalid_registrations[1]).is_valid()

    def test_invalid_registration_email_already_exists_error(self):
        form = RegistrationForm()
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

        form = RegistrationForm(data=data)

        assert True is ('User account with this Email already exists.' in str(form.errors))
        assert False is form.is_valid()

    def test_invalid_registration_username_already_exists_error(self):
        form = RegistrationForm()
        assert False is form.is_valid()

        data = {
            "email": "user1unique@testmail.com",
            "username": "username1",
            "password1": "Password56",
            "password2": "Password56",
            "first_name": "Hello",
            "last_name": "Hello",
            "address_x": "-343",
            "phone_number": "0824255626",
            "address_y": "43"
        }

        form = RegistrationForm(data=data)

        assert ('User account with this Username already exists.' in str(form.errors))
        assert False is form.is_valid()

    def test_invalid_registration_passwords_dont_match(self):
        form = RegistrationForm()
        assert False is form.is_valid()

        data = {
            "email": "user1uniqueed@testmail.com",
            "username": "username1111",
            "password1": "Password56",
            "password2": "hellohello45",
            "first_name": "Hello",
            "last_name": "Hello",
            "address_x": "-343",
            "phone_number": "0824255626",
            "address_y": "43"
        }

        form = RegistrationForm(data=data)

        assert ('password fields didn’t match' in str(form.errors))
        assert False is form.is_valid()
