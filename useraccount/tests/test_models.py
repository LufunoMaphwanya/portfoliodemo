import unittest

from django.test import TestCase

from useraccount.models import UserAccount

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        for i in range(0,10):
            UserAccount.objects.create(
                email=f"user{i}@testmail.com",
                username=f"username{i}",
                first_name=f"person-{i}",
                last_name=f"person-{i}",
                phone_number=f"surname-{i}",
                address_x=f"400",
                address_y=f"-200",
            )

    def test_first_name_max_length(self):
        author = UserAccount.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        user = UserAccount.objects.get(id=1)
        expected_object_name = f'{user.email}'
        self.assertEqual(str(user), expected_object_name)

    @unittest.expectedFailure
    def test_unique_email(self):

        i = 1
        ua = UserAccount.objects.create(
            email=f"user{i}@testmail.com",
            username=f"username{i}",
            first_name=f"person-{i}",
            last_name=f"person-{i}",
            phone_number=f"surname-{i}",
            address_x=f"400",
            address_y=f"-200",
        )

        ua.save()


