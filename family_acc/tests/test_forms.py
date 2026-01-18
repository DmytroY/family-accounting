import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from transactions.models import Currency, Account, Category, Transaction


# class CurrencyFormTest(TestCase):
#     def setUp(self):
#         # creaTe user and login
#         self.user = User.objects.create_user(username='testuser', password="testuserpass123")
#         self.profile = self.user.profile
#         self.user.profile.family = "testuserfamily"
#         self.user.profile.save()
#         self.client.login(username='testuser', password="testuserpass123")

#     def test_create_currency(self):
#         form_data = {
#             'code': 'XYZ',
#             'description': 'test currency description'
#         }
#         response = self.client.post(reverse('transactions:currency_create'), data=form_data)
#         self.assertRedirects(response, '/transactions/currency_list', status_code=302, target_status_code=200)
#         self.assertTrue(Currency.objects.filter(code='XYZ').exists())
#         self.assertTrue(Currency.objects.filter(description='test currency description').exists())

#     def test_edit_currency(self):
#         cur = Currency.objects.create(
#             code='XYZ',
#             description='test currency description',
#             family=self.user.profile.family)
#         form_data = {
#             'code': 'AAA',
#             'description': 'edited test currency description'
#         }
#         url = reverse('transactions:currency_edit', args=[cur.id])
#         response = self.client.post(url, data=form_data)
#         self.assertRedirects(response, '/transactions/currency_list', status_code=302, target_status_code=200) 
#         self.assertFalse(Currency.objects.filter(code='XYZ').exists())
#         self.assertFalse(Currency.objects.filter(description='test currency description').exists())

#         self.assertTrue(Currency.objects.filter(code='AAA').exists())
#         self.assertTrue(Currency.objects.filter(description='edited test currency description').exists())

#     def test_delete_currency(self):
#         cur = Currency.objects.create(
#             code='XYZ',
#             description='test currency description',
#             family=self.user.profile.family)
#         url = reverse('transactions:currency_edit', args=[cur.id])
#         response = self.client.post(url, data={'action': 'delete'})
#         self.assertRedirects(response, '/transactions/currency_list', status_code=302, target_status_code=200) 
#         self.assertFalse(Currency.objects.filter(code='XYZ').exists())
#         self.assertFalse(Currency.objects.filter(description='test currency description').exists())


# class AccountFormTest(TestCase):
#     def setUp(self):
#         # create user
#         self.user = User.objects.create_user(username='testuser', password="testuserpass123")
#         self.profile = self.user.profile
#         self.user.profile.family = "testuserfamily"
#         self.user.profile.save()
#         # login required othervise attempt to access form will result in redirect to login page
#         self.client.login(username='testuser', password="testuserpass123")
#         # create currency required for account
#         self.cur = Currency.objects.create(
#             code='XYZ',
#             description='test currency description',
#             family=self.user.profile.family)

#     def test_create_account(self):
#         form_data = {
#             'name': 'Test Account',
#             'balance': 99,
#             'currency': self.cur.id
#         }

#         response = self.client.post(reverse('transactions:account_create'), data=form_data)
#         self.assertRedirects(response, '/transactions/account_list', status_code=302, target_status_code=200)
#         self.assertTrue(Account.objects.filter(name='Test Account').exists())
#         self.assertTrue(Account.objects.filter(balance=99).exists())

#     def test_edit_account(self):
#         acc = Account.objects.create(
#             name='Account initial name',
#             balance= - 55.55,
#             currency=self.cur
#         )
#         form_data = {
#             'name': 'Changed name for account',
#             'balance': 99.99,
#             'currency': self.cur.id
#         }
#         url = reverse('transactions:account_edit', args=[acc.id])
#         response = self.client.post(url, data=form_data)
#         self.assertRedirects(response, '/transactions/account_list', status_code=302, target_status_code=200)
#         self.assertTrue(Account.objects.filter(name='Changed name for account').exists())
#         self.assertTrue(Account.objects.filter(balance=99.99).exists())

#     def test_account_delete(self):
#         acc = Account.objects.create(
#             name='Account initial name',
#             balance= -55.55,
#             currency=self.cur
#         )
#         response = self.client.post(reverse('transactions:account_edit', args=[acc.id]), data={'action': 'delete'})
#         self.assertRedirects(response, '/transactions/account_list', status_code=302, target_status_code=200)
#         self.assertFalse(Account.objects.filter(name='Account initial name').exists())
#         self.assertFalse(Account.objects.filter(balance= -55.55).exists())

# class CategoryFormTest(TestCase):
#     def setUp(self):
#         # creaTe user and login
#         self.user = User.objects.create_user(username='testuser', password="testuserpass123")
#         self.profile = self.user.profile
#         self.user.profile.family = "testuserfamily"
#         self.user.profile.save()
#         self.client.login(username='testuser', password="testuserpass123")

#     def test_category_create(self):
#         form_data = {
#             'name': 'Test category',
#             'income_flag': True,
#             'expense_flag': False
#         }
#         url = reverse('transactions:category_create')
#         response = self.client.post(url, data=form_data)
#         self.assertRedirects(response, '/transactions/category_list', status_code=302, target_status_code=200)
#         cat = Category.objects.get(name='Test category')
#         self.assertEqual(cat.income_flag, True)
#         self.assertEqual(cat.expense_flag, False)
        
#     def test_category_edit(self):
#         cat = Category.objects.create(
#             name='Initial category',
#             income_flag=True,
#             expense_flag=False
#         )
#         form_data = {
#             'name': 'Changed category',
#             'income_flag': False,
#             'expense_flag': True
#         }
#         url = reverse('transactions:category_edit', args=[cat.id])
#         response = self.client.post(url, data=form_data)
#         self.assertRedirects(response, '/transactions/category_list', status_code=302, target_status_code=200)
#         cat2 = Category.objects.get(id=cat.id)
#         self.assertEqual(cat2.name, 'Changed category')
#         self.assertEqual(cat2.income_flag, False)
#         self.assertEqual(cat2.expense_flag, True)

#     def test_category_delete(self):
#         cat = Category.objects.create(
#             name='Initial category',
#             income_flag=True,
#             expense_flag=False
#         )
#         url = reverse('transactions:category_edit', args=[cat.id])
#         response = self.client.post(url, data={'action': 'delete'})
#         self.assertRedirects(response, '/transactions/category_list', status_code=302, target_status_code=200)
#         self.assertFalse(Category.objects.filter(name='Initial category').exists())

class TransactionFormTest(TestCase):
    def setUp(self):
        # create user and login
        self.user = User.objects.create_user(username='testuser', password="testuserpass123")
        self.profile = self.user.profile
        self.user.profile.family = "testuserfamily"
        self.user.profile.save()
        self.client.login(username='testuser', password="testuserpass123")
        # create currency required for account
        self.cur = Currency.objects.create(
            code='XYZ',
            description='test currency description',
            family=self.user.profile.family)
        # create account
        self.acc = Account.objects.create(
            name='Test account',
            balance=Decimal('0'),
            currency=self.cur,
            family=self.user.profile.family
        )
        # create categories
        self.cat_inc = Category.objects.create(
            name='Category for income',
            income_flag=True,
            expense_flag=False,
            family=self.user.profile.family
            )
        self.cat_exp = Category.objects.create(
            name='Category for expense',
            income_flag=False,
            expense_flag=True,
            family=self.user.profile.family
            )
        
    def test_transaction_create_income(self):
        form_data = {
            'date': '2025-06-30',
            'currency': self.cur.id,
            'account': self.acc.id,
            'amount': -33.33, # create income form must convert it to positive am't
            'category': self.cat_inc.id,
            'remark': 'remark for test income transaction'
        }
        url = reverse('transactions:transaction_create', kwargs={'transaction_type': 'income'})
        response = self.client.post(url, data=form_data)
        self.assertRedirects(response, '/transactions/transaction_list', status_code=302, target_status_code=200)
        tr = Transaction.objects.get(remark='remark for test income transaction')
        # asserting transaction created
        self.assertEqual(tr.date, datetime.date(2025, 6, 30))
        self.assertEqual(tr.account, self.acc)
        self.assertEqual(tr.amount, Decimal('33.33'))
        self.assertEqual(tr.category, self.cat_inc)
        # asserting Account balance properly adjusted
        self.acc.refresh_from_db()  # Refresh the account instance from the database
        self.assertEqual(self.acc.balance, Decimal('33.33'))

    def test_transaction_create_expense(self):
        form_data = {
            'date': '2025-05-15',
            'currency': self.cur.id,
            'account': self.acc.id,
            'amount': 123.45, # create expense form must convert it to negative am't
            'category': self.cat_exp.id,
            'remark': 'remark for test expense transaction'
        }
        url = reverse('transactions:transaction_create', kwargs={'transaction_type': 'expense'})
        response = self.client.post(url, data=form_data)
        self.assertRedirects(response, '/transactions/transaction_list', status_code=302, target_status_code=200)
        tr = Transaction.objects.get(remark='remark for test expense transaction')
        self.assertEqual(tr.date, datetime.date(2025, 5, 15))
        self.assertEqual(tr.account, self.acc)
        self.assertEqual(tr.amount, Decimal('-123.45'))
        self.assertEqual(tr.category, self.cat_exp)
        # asserting Account balance properly adjusted
        self.acc.refresh_from_db()  # Refresh the account instance from the database
        self.assertEqual(self.acc.balance, Decimal('-123.45'))

    def test_transaction_edit(self):
        tr = Transaction.objects.create(
            date = datetime.date(2025, 5, 15),
            account = self.acc,
            amount = Decimal('-123.45'),
            currency = self.cur,
            category = self.cat_exp,
            remark = 'transaction before update',
            created_by = self.user
        )
        form_data = {
            'date': '2025-02-01',
            'currency': self.cur.id,
            'account': self.acc.id,
            'amount': 1.11, # create expense form must convert it to negative am't
            'category': self.cat_exp.id,
            'remark': 'transaction after update'
        }
        url = reverse('transactions:transaction_edit', args=[tr.id])
        response = self.client.post(url, data={'action': 'save', **form_data})
        self.assertRedirects(response, '/transactions/transaction_list', status_code=302, target_status_code=200)
        tr.refresh_from_db()
        self.assertEqual(tr.date, datetime.date(2025, 2, 1))
        self.assertEqual(tr.amount, Decimal('-1.11'))
        self.assertEqual(tr.remark,'transaction after update')

    def test_transaction_delete(self):
        tr = Transaction.objects.create(
            date = datetime.date(2025, 5, 15),
            account = self.acc,
            amount = Decimal('-123.45'),
            currency = self.cur,
            category = self.cat_exp,
            remark = 'transaction before update',
            created_by = self.user
        )
        url = reverse('transactions:transaction_edit', args=[tr.id])
        response = self.client.post(url, data={'action': 'delete'})
        self.assertRedirects(response, '/transactions/transaction_list', status_code=302, target_status_code=200)
        self.assertFalse(Transaction.objects.filter(remark = 'transaction before update').exists())