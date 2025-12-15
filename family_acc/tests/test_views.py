from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from transactions.models import Currency, Account, Category, Transaction
from django.urls import reverse
from datetime import date

class TestHomePage(SimpleTestCase):

    def test_homepage_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_homapage_message(self):
        response = self.client.get('/')
        self.assertContains(response, 'This is home p', status_code=200)

class TestTransactionsPage(TestCase):
    def setUp(self):
        # thransaction view accessible only for authenticated users, need to login
        self.user = User.objects.create_user(username='testuser', password="testuserpass123")
        self.client.login(username='testuser', password="testuserpass123")

        # Assign the profile and set the family field
        self.profile = self.user.profile
        self.user.profile.family = "testuserfamily"
        self.user.profile.save()
        
        # creating transaction record
        self.currency = Currency.objects.create(code='CZK', description='Czech koruna')
        self.account = Account.objects.create(name='Cash', balance=555, currency=self.currency)
        self.category = Category.objects.create(name='Other imcomes', income_flag=True, expense_flag=False)
        self.transaction = Transaction.objects.create(
            date=date.today().strftime("%Y-%m-%d"),
            account=self.account,
            amount='1001.99',
            currency=self.currency,
            category=self.category,
            remark='test remark',
            created_by=self.user,
            family=self.profile.family)

    def test_transactions_uses_template(self):
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertTemplateUsed(response, 'transaction_list.html')

    def test_transactions_uses_authorised_user(self):
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertContains(response, 'You authorized as', status_code=200)
        self.assertContains(response, 'testuser', status_code=200)

    def test_transactions_shows_record(self):
        response = self.client.get(reverse('transactions:transaction_list'))
        self.assertContains(response, '<h1>Transactions</h1>')
        self.assertContains(response, date.today().strftime("%d-%m-%Y"))
        self.assertContains(response, '1001.99')
        self.assertContains(response, 'CZK')
        self.assertContains(response, 'Other imcomes')

