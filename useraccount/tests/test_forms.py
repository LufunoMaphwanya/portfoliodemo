
from useraccount.forms import RegistrationForm
from django.test import TestCase


class TestForms(TestCase):
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
                "password2": "Testing1234", # passwords do not match
                "first_name": "Hello",
                "last_name": "Hello",
                "address_x": "-343",
                "address_y": "43"
            },
            {
                "password1": "Password56",
                "password2": "Password56",
                "first_name": "Hello",
                "last_name": "Hello", # no email/username provided
                "address_x": "-343",
                "address_y": "43"
            }
        ]


        assert False is RegistrationForm(data=invalid_registrations[0]).is_valid()
        assert False is RegistrationForm(data=invalid_registrations[1]).is_valid()
