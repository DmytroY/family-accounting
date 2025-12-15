from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class SelfRegisterAPITest(APITestCase):
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

        self.assertContains(response, "user created", status_code=201)

        user = User.objects.get(username="test_user7564")
        self.assertEqual(user.first_name, "test_user_firstname")
        self.assertEqual(user.last_name, "test_user_lastname")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertTrue(len(user.profile.family))

class ObtainTokenAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u0", password="s8am3n")
        self.url = "/api/token/"

    def test_obtain_token_success(self):
        data = {"username": "u0", "password": "s8am3n",}
        response = self.client.post(self.url, data)
        self.assertContains(response, "token", status_code=200)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data["token"], token.key)

    def test_obtain_token_wrong_password(self):
        data = {"username": "u0", "password": "wrongpassword",}
        response = self.client.post(self.url, data)
        self.assertContains(response, "error", status_code=400)


class MemberListAPI(APITestCase):
    def setUp(self):
        self.user0 = User.objects.create_user(username="u0", password="s8am3n")
        self.user0.profile.family = "family1"
        self.user0.save()

        self.user1 = User.objects.create_user(username="u1", password="s8am3n")
        self.user1.profile.family = "family1"
        self.user1.save()

        self.user_otherfamily = User.objects.create_user(username="u_other", password="s8am3n")
        self.user_otherfamily.profile.family = "otherfamily"
        self.user_otherfamily.save()

        self.token = Token.objects.create(user=self.user0)
        self.url = reverse("members:api_members")

    def test_member_list_get_w_authentication_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        users = set()
        for u in response.data:
            users.add(u["username"])
        self.assertSetEqual(users, {'u0', 'u1'})

    def test_member_list_no_token(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Authentication credentials were not provided.", status_code=403)
    
    def test_member_list_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token s0mewr0ngt0ken")
        response = self.client.get(self.url)
        # print(f"--DY-- response.data: {response.data}")
        self.assertContains(response, "Invalid token", status_code=403)



