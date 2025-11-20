from django.test import TestCase
from django.contrib.auth.models import User
from transactions.models import Currency, Account, Category, Transaction
from members.models import Profile

class MembersModelsTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password="testuserpass123")
        self.profile = self.user.profile
        self.user.profile.family = "testuserfamily"
        self.user.profile.save()
        self.client.login(username='testuser', password="testuserpass123")

    def test_user_created(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_userprofile_reated(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.family, "testuserfamily")
    
class TransactionsModelsTest(TestCase):

    def setUp(self):
        self.currency = Currency(code='CZK', description='Czech koruna')
        self.account = Account(name='Cash', balance=555, currency=self.currency)
        self.category = Category(name='Other imcomes', income_flag=True, expense_flag=False)

    def test_currency(self):
        self.assertEqual(self.currency.description, 'Czech koruna')
        self.assertEqual(str(self.currency), 'CZK')

    def test_account(self):
        self.assertEqual(self.account.balance, 555)
        self.assertEqual(str(self.account), 'Cash')
        self.assertEqual(self.account.currency, self.currency)

    def test_category(self):
        self.assertTrue(self.category.income_flag)
        self.assertFalse(self.category.expense_flag)
        self.assertEqual(str(self.category), 'Other imcomes')
    
    def test_transaction(self):
        self.transaction = Transaction(
            date='2025-06-30',
            account=self.account,
            amount='1000',
            currency=self.currency,
            category=self.category,
            remark='test remark',
            created_by=None,
            family=None)
        self.assertEqual(str(self.transaction), f"2025-06-30  {self.account}  1000  {self.currency}  {self.category}")