from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from transactions.models import Currency, Account, Category, Transaction


class LoginRequiredForAnyNotHomePage(TestCase):
    def test_redirect_to_login(self):

        response = self.client.post(reverse('members:list'))
        self.assertRedirects(response, '/members/login/?next=/members/', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:transaction_list'))
        self.assertRedirects(response, '/members/login/?next=/transactions/transaction_list', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:transaction_create_expense'))
        self.assertRedirects(response, '/members/login/?next=/transactions/transaction_create_expense', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:transaction_create_income'))
        self.assertRedirects(response, '/members/login/?next=/transactions/transaction_create_income', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:account_list'))
        self.assertRedirects(response, '/members/login/?next=/transactions/account_list', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:account_create'))
        self.assertRedirects(response, '/members/login/?next=/transactions/account_create', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:category_list'))
        self.assertRedirects(response, '/members/login/?next=/transactions/category_list', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:category_create'))
        self.assertRedirects(response, '/members/login/?next=/transactions/category_create', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:currency_list'))
        self.assertRedirects(response, '/members/login/?next=/transactions/currency_list', status_code=302, target_status_code=200)

        response = self.client.post(reverse('transactions:currency_create'))
        self.assertRedirects(response, '/members/login/?next=/transactions/currency_create', status_code=302, target_status_code=200)

class AnyPageAccessibleForAuthorisedUser(TestCase):
    def setUp(self):
        # create user
        self.user = User.objects.create_user(username='testuser', password="testuserpass123")
        self.profile = self.user.profile
        self.user.profile.family = "testuserfamily"
        self.user.profile.save()
        #log in
        self.client.login(username='testuser', password="testuserpass123")

    def test_(self):
        response = self.client.post(reverse('members:list'))
        self.assertTemplateUsed(response, 'all_members.html')
        self.assertContains(response, f'List of family {self.user.profile.family} members', status_code=200)
       