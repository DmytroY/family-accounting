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

    def test_access_after_login(self):
        response = self.client.post(reverse('members:list'))
        self.assertTemplateUsed(response, 'all_members.html')
        self.assertContains(response, f'List of family {self.user.profile.family} members', status_code=200)

        response = self.client.post(reverse('transactions:transaction_list'))
        self.assertTemplateUsed(response, 'transaction_list.html')
        self.assertContains(response, f'Last transactions', status_code=200)

        response = self.client.post(reverse('transactions:transaction_create_expense'))
        self.assertTemplateUsed(response, 'transaction_create_expense.html')
        self.assertContains(response, f'Add new expense', status_code=200)

        response = self.client.post(reverse('transactions:transaction_create_income'))
        self.assertTemplateUsed(response, 'transaction_create_income.html')
        self.assertContains(response, f'Add new income', status_code=200)

        response = self.client.post(reverse('transactions:account_list'))
        self.assertTemplateUsed(response, 'account_list.html')
        self.assertContains(response, f'Accounts of family', status_code=200)

        response = self.client.post(reverse('transactions:account_create'))
        self.assertTemplateUsed(response, 'account_create.html')
        self.assertContains(response, f'Create new account', status_code=200)

        response = self.client.post(reverse('transactions:category_list'))
        self.assertTemplateUsed(response, 'category_list.html')
        self.assertContains(response, f'Categories of income/expenses used by', status_code=200)

        response = self.client.post(reverse('transactions:category_create'))
        self.assertTemplateUsed(response, 'category_create.html')
        self.assertContains(response, f'Create new category record', status_code=200)

        response = self.client.post(reverse('transactions:currency_list'))
        self.assertTemplateUsed(response, 'currency_list.html')
        self.assertContains(response, f'Currency used by', status_code=200)

        response = self.client.post(reverse('transactions:currency_create'))
        self.assertTemplateUsed(response, 'currency_create.html')
        self.assertContains(response, f'Create new currency record', status_code=200)

class UserHasAccessOnlyOwnFamilyRecords(TestCase):
    def setUp(self):
        # create users in different families
        self.user1 = User.objects.create_user(username='testuser1', password="testuserpass1")
        self.profile = self.user1.profile
        self.user1.profile.family = "family1"
        self.user1.profile.save()

        self.user2 = User.objects.create_user(username='testuser2', password="testuserpass2")
        self.profile = self.user2.profile
        self.user2.profile.family = "family2"
        self.user2.profile.save()

        # creating records in family of testuser1
        self.currency = Currency.objects.create(code='XYZ', description='XYZ is test currency', family=self.user1.profile.family)
        self.account = Account.objects.create(name='Test Account, XYZ currency', balance=555, currency=self.currency, family=self.user1.profile.family)
        self.category = Category.objects.create(name='Test imcome categoryXYZ', income_flag=True, expense_flag=False, family=self.user1.profile.family)
        self.transaction = Transaction.objects.create(
            date='2025-06-30',
            account=self.account,
            amount='1001.99',
            currency=self.currency,
            category=self.category,
            remark='test remark',
            created_by=self.user1,
            family=self.user1.profile.family)

        #log in as user1
        self.client.login(username='testuser1', password="testuserpass1")

    def test_testuser1_has_access_to_family1_data(self):
        response = self.client.post(reverse('members:list'))
        self.assertContains(response, f'title="push to see details">{self.user1.username}', status_code=200)

        response = self.client.post(reverse('transactions:transaction_list'))
        self.assertContains(response, f'1001.99', status_code=200)

        response = self.client.post(reverse('transactions:account_list'))
        self.assertContains(response, f'Test Account, XYZ currency', status_code=200)

        response = self.client.post(reverse('transactions:category_list'))
        self.assertContains(response, f'Test imcome categoryXYZ', status_code=200)

        response = self.client.post(reverse('transactions:currency_list'))
        self.assertContains(response, f'XYZ is test currency', status_code=200)

    def test_testuser2_has_NO_access_to_family1_data(self):
        self.client.logout()
        self.client.login(username='testuser2', password="testuserpass2")

        response = self.client.post(reverse('members:list'))
        self.assertNotContains(response, f'title="push to see details">{self.user1.username}', status_code=200)

        response = self.client.post(reverse('transactions:transaction_list'))
        self.assertNotContains(response, f'1001.99', status_code=200)

        response = self.client.post(reverse('transactions:account_list'))
        self.assertNotContains(response, f'Test Account, XYZ currency', status_code=200)

        response = self.client.post(reverse('transactions:category_list'))
        self.assertNotContains(response, f'Test imcome categoryXYZ', status_code=200)

        response = self.client.post(reverse('transactions:currency_list'))
        self.assertNotContains(response, f'XYZ is test currency', status_code=200)

