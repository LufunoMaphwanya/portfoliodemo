from django.test import TestCase
from django.urls import reverse


from useraccount.forms import LoginForm, RegistrationForm
from useraccount.models import UserAccount



class AccountListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = [ UserAccount.objects.create(
                email=f"user{i}@testmail.com",
                username=f"username{i}",
                first_name=f"person-{i}",
                last_name=f"person-{i}",
                phone_number=f"surname-{i}",
                password=f"password",
                address_x=f"400",
                address_y=f"-200",
            ) for i in range(0, 20) ]

        [_.save() for _ in users]

    '''
    Guest context tests
    No user login
    '''
    def test_landing_page(self):
        response = self.client.get('')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'useraccount/home.html')

    def test_login_page_returns_with_login_form(self):
        response = self.client.get('/login')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'useraccount/login.html')

        self.assertEqual(type(response.context['login_form']), LoginForm)

    def test_register_page_returns_with_registration_form(self):
        response = self.client.get('/register')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'useraccount/register.html')

        self.assertEqual(type(response.context['registration_form']), RegistrationForm)


    def test_redirects_to_login_protected_pages(self):
        protected_pages = ['network', 'profile']

        response1 = self.client.get(reverse(protected_pages[0]))
        response2 = self.client.get(reverse(protected_pages[1]))

        self.assertEqual(
            (response1.status_code, response2.status_code),
            (302, 302)
        )

    '''
    Logged in  User context    
    '''
