from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from transactions.models import Currency, Account, Category, Transaction


class CurrencyFormTest(TestCase):
    def setUp(self):
        # creaTe user and login
        self.user = User.objects.create_user(username='testuser', password="testuserpass123")
        self.profile = self.user.profile
        self.user.profile.family = "testuserfamily"
        self.user.profile.save()
        self.client.login(username='testuser', password="testuserpass123")

    def test_create_currency(self):
        form_data = {
            'code': 'XYZ',
            'description': 'test currency description'
        }
        response = self.client.post(reverse('transactions:currency_create'), data=form_data)
        self.assertRedirects(response, '/transactions/currency_list', status_code=302, target_status_code=200)
        self.assertTrue(Currency.objects.filter(code='XYZ').exists())
        self.assertTrue(Currency.objects.filter(description='test currency description').exists())

    def test_edit_currency(self):
        cur = Currency.objects.create(
            code='XYZ',
            description='test currency description',
            family=self.user.profile.family)
        form_data = {
            'code': 'AAA',
            'description': 'edited test currency description'
        }
        url = reverse('transactions:currency_edit', args=[cur.id])
        response = self.client.post(url, data=form_data)
        self.assertRedirects(response, '/transactions/currency_list', status_code=302, target_status_code=200) 
        self.assertFalse(Currency.objects.filter(code='XYZ').exists())
        self.assertFalse(Currency.objects.filter(description='test currency description').exists())

        self.assertTrue(Currency.objects.filter(code='AAA').exists())
        self.assertTrue(Currency.objects.filter(description='edited test currency description').exists())

    def test_delete_currency(self):
        cur = Currency.objects.create(
            code='XYZ',
            description='test currency description',
            family=self.user.profile.family)
        url = reverse('transactions:currency_edit', args=[cur.id])
        response = self.client.post(url, data={'action': 'delete'})
        self.assertRedirects(response, '/transactions/currency_list', status_code=302, target_status_code=200) 
        self.assertFalse(Currency.objects.filter(code='XYZ').exists())
        self.assertFalse(Currency.objects.filter(description='test currency description').exists())