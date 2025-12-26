from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from transactions.models import Currency, Account, Category, Transaction
from decimal import *

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

class TransactionCreateAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)

        cur = Currency.objects.create(code="USD", description="US Dollar", family="fam1")
        self.acc = Account.objects.create(name="Test bank account", balance=10000, currency=cur, family="fam1")
        self.cat_inc = Category.objects.create(name="Test income categ", income_flag=True, expense_flag=False, family="fam1")
        self.cat_exp = Category.objects.create(name="Test expense categ", income_flag=False, expense_flag=True, family="fam1")

    def test_create_income(self):
        self.url = reverse('transactions:api_income_create')
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "date":"2025-12-23",
            "account": self.acc.id,
            "amount":-11.99,
            "category":"Test income categ",
            "remark":"some remark to income transaction"
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertTrue(Transaction.objects.filter(date="2025-12-23", account=self.acc.id, amount=11.99, category=self.cat_inc, remark="some remark to income transaction", family="fam1").exists())
        self.assertEqual(Account.objects.get(name="Test bank account", family="fam1").balance, Decimal("10011.99"))
        self.assertContains(response, "income created", status_code=status.HTTP_201_CREATED)

    def test_create_expense(self):
        self.url = reverse('transactions:api_expense_create')
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {
            "date":"2025-12-23",
            "account": self.acc.id,
            "amount": 555.45,
            "category":"Test expense categ",
            "remark":"some remark to expense transaction"
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertTrue(Transaction.objects.filter(date="2025-12-23", account=self.acc.id, amount=-555.45, category=self.cat_exp, remark="some remark to expense transaction", family="fam1").exists())
        self.assertEqual(Account.objects.get(name="Test bank account", family="fam1").balance, Decimal("9444.55"))
        self.assertContains(response, "expense created", status_code=status.HTTP_201_CREATED)

class TransactionListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.user.profile.family = "fam1"
        self.user.profile.save()
        self.token = Token.objects.create(user=self.user)
        cur = Currency.objects.create(code="USD", description="US Dollar", family="fam1")
        self.acc = Account.objects.create(name="Test bank account", balance=0, currency=cur, family="fam1")
        self.cat_inc = Category.objects.create(name="Test income categ", income_flag=True, expense_flag=False, family="fam1")
        self.cat_exp = Category.objects.create(name="Test expense categ", income_flag=False, expense_flag=True, family="fam1")
        Transaction.objects.create(date="2025-12-01", account=self.acc, amount=1001.55, currency=cur, category=self.cat_inc, remark="remark 1", created_by=self.user)
        Transaction.objects.create(date="2025-12-15", account=self.acc, amount=1.44, currency=cur,category=self.cat_exp, remark="remark 2", created_by=self.user)
    
        self.user_other = User.objects.create_user(username="other", password="3daq43pa")
        self.user_other.profile.family = "othet_fam"
        self.user_other.profile.save()
        cur_other = Currency.objects.create(code="USD", description="US Dollar othet_fam", family="othet_fam")
        self.acc_other = Account.objects.create(name="Test bank account othet_fam", balance=0, currency=cur_other, family="othet_fam")
        self.cat_other = Category.objects.create(name="Test income categ othet_fam", income_flag=True, expense_flag=False, family="othet_fam")
        Transaction.objects.create(date="2025-12-10", account=self.acc_other, amount=999.99, currency=cur_other, category=self.cat_other, remark="oter family transaction", created_by=self.user_other)

        self.url = reverse('transactions:api_transaction_list')
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_list_all_transactions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        remarks = { a["remark"] for a in response.data}
        self.assertSetEqual(remarks, {"remark 1", "remark 2"})

    def test_filter_by_date1(self):
        response = self.client.get(self.url, {"from": "2025-12-01", "to": "2025-12-14"})
        self.assertEqual(len(response.data), 1)
        # print(f"--DY-- type(response.data), response.data: {type(response.data), response.data}")
        self.assertEqual(response.data[0]["date"], "2025-12-01")

    def test_filter_by_date2(self):
        response = self.client.get(self.url, {"from": "2025-12-02", "to": "2025-12-15"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["date"], "2025-12-15")

    def test_filter_by_account_id(self):
        response = self.client.get(self.url, {"account_id": self.acc.id})
        self.assertEqual(len(response.data), 2)

    def test_filter_by_account_name(self):
        response = self.client.get(self.url, {"account": "Test bank account"})
        self.assertEqual(len(response.data), 2)

    def test_filter_by_category_name(self):
        response = self.client.get(self.url, {"category": "Test income categ"})
        self.assertEqual(len(response.data), 1)

    def test_filter_by_currency_code(self):
        response = self.client.get(self.url, {"currency": "USD"})
        self.assertEqual(len(response.data), 2)

    def test_filter_no_results(self):
        response = self.client.get(self.url, {"category": "NonExisting"})
        self.assertEqual(len(response.data), 0)