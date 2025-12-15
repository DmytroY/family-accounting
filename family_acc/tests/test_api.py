from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class SelfRegisterViaAPI(APITestCase):
    def test_register_user(self):
        url = reverse("members:api_register")
        data = {
            "first_name": "test_user_firstname",
            "last_name": "test_user_lastname",
            "email": "testuser@email.com",
            "username": "test_user7564",
            "password1": "d98.rns%",
            "password2": "d98.rns%",
        }
        response = self.client.post(url, data, format="json")
        # print(response.data)

        self.assertContains(response, "user created", status_code=201)

        user = User.objects.get(username="test_user7564")
        self.assertEqual(user.first_name, "test_user_firstname")
        self.assertEqual(user.last_name, "test_user_lastname")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertTrue(len(user.profile.family))
