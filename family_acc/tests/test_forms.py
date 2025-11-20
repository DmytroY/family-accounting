from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from transactions.models import Currency, Account, Category, Transaction


class LoginRequiredForAnyForms(TestCase):
    def test_redirect_to_login(self):
        response = self.client.post(reverse('transactions:currency_create'))
        self.assertRedirects(response, '/members/login/?next=/transactions/currency_create', status_code=302, target_status_code=200)


# class CurrencyFormTest(TestCase):
#     def test_create_currency(self):
#         form_data = {
#             'code': 'XYZ',
#             'description': 'test currency description'
#         }
#         response = self.client.post(reverse('transactions:currency_create'), data=form_data)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(Currency.objects.filter(code='XYZ').exists())