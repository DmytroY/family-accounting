from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from transactions.models import Currency, Account, Category, Transaction
from django.urls import reverse

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
        self.currency = Currency.objects.create(code='CZK', descr='Czech koruna')
        self.account = Account.objects.create(name='Cash', balance=555)
        self.category = Category.objects.create(name='Other imcomes', income_flag=True, expence_flag=False)
        self.transaction = Transaction.objects.create(
            date='2025-06-30',
            account=self.account,
            amount='1000',
            currency=self.currency,
            category=self.category,
            remark='test remark',
            created_by=self.user,
            family=self.profile.family)

    def test_transactions_uses_template(self):
        response = self.client.get(reverse('transactions:list'))
        self.assertTemplateUsed(response, 'list.html')

    def test_transactions_uses_authorised_user(self):
        response = self.client.get(reverse('transactions:list'))
        self.assertContains(response, 'You authorized as testuser', status_code=200)

    def test_transactions_shows_record(self):
        response = self.client.get(reverse('transactions:list'))
        self.assertContains(response, 'test remark')

