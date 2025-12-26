from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from transactions.models import Currency, Account, Category, Transaction

class CurrencyListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)

        Currency.objects.create(code="USD", description="US Dollar", family="fam1")
        Currency.objects.create(code="CZK", description="Czech Koruna", family="fam1")
        Currency.objects.create(code="EUR", description="Euro", family="other")

        self.url = reverse('transactions:api_currency_list')

    def test_get_currency_list(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        codes = {c["code"] for c in response.data}
        self.assertSetEqual(codes, {"USD", "CZK"})

class CurrencyCreateAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)

        self.url = reverse('transactions:api_currency_create')

    def test_create_currency(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "code": "USD",
            "description": "US dollar",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertTrue(Currency.objects.filter(code="USD", family="fam1").exists())
        self.assertContains(response, "currency created", status_code=status.HTTP_201_CREATED)


class AccountCreateAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)

        Currency.objects.create(code="USD", description="US Dollar", family="fam1")

        self.url = reverse('transactions:api_account_create')
    
    def test_create_account(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "name": "Test bank account",
            "balance": 33,
            "currency": "USD",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(Account.objects.get(name="Test bank account", family="fam1").balance, 33)
        self.assertContains(response, "account created", status_code=status.HTTP_201_CREATED)

class AccountListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)

        cur = Currency.objects.create(code="USD", description="US Dollar", family="fam1")

        Account.objects.create(name="Test bank account 1", balance=33, currency=cur, family="fam1")
        Account.objects.create(name="Test bank account 2", balance=0, currency=cur, family="fam1")
        Account.objects.create(name="Other family account", balance=0, currency=cur, family="other")

        self.url = reverse('transactions:api_account_list')

    def test_get_accounts(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(self.url)

        self.assertContains(response, "33.00", status_code=status.HTTP_200_OK)
        acc_names = { a["name"] for a in response.data}
        self.assertSetEqual(acc_names, {"Test bank account 1", "Test bank account 2"})

class CategoryListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)

        Category.objects.create(name="Test income categ", income_flag=True, expense_flag=False, family="fam1")
        Category.objects.create(name="Test expense categ", income_flag=False, expense_flag=True, family="fam1")
        Category.objects.create(name="Other family categ", income_flag=True, expense_flag=True, family="other")

        self.url = reverse('transactions:api_category_list')
    
    def test_get_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        acc_names = { a["name"] for a in response.data}
        self.assertSetEqual(acc_names, {"Test income categ", "Test expense categ"})

class CategoryCreateAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)

        self.url = reverse('transactions:api_category_create')

    def test_create_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "name":"Test income categ", 
            "income_flag": True, 
            "expense_flag": False,
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertTrue(Category.objects.filter(name="Test income categ", family="fam1").exists())
        self.assertContains(response, "category created", status_code=status.HTTP_201_CREATED)
