from django.test import TestCase
from django.urls import reverse

from useraccount.models import UserAccount

class AccountListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        for i in range(0, 20):
            UserAccount.objects.create(
                email=f"user{i}@testmail.com",
                username=f"username{i}",
                first_name=f"person-{i}",
                last_name=f"person-{i}",
                phone_number=f"surname-{i}",
                address_x=f"400",
                address_y=f"-200",
            )
    def test_redirects_to_login_protected_pages(self):

        protected_pages = ['network', 'profile']

        response1 = self.client.get(reverse(protected_pages[0]))
        response2 = self.client.get(reverse(protected_pages[1]))

        self.assertEqual(
            (response1.status_code, response2.status_code),
            (302, 302) #redirects to login
        )

