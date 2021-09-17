from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "example@example.com",
            "username": "demousername",
            "password": "demopassword",
        }
        self.base_user = User.objects.create_user(**self.user_data)
        self.client = APIClient()

    def test_signup(self):
        url = "/api/signup/"
        payload = {
            **self.user_data,
            "email": "change@example.com",
            "username": "change",
        }
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """Test Duplicate email """
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        url = "/api/login/"
        payload = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """Test With worong credintial"""
        payload["password"] = "unknownpassword"
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile(self):
        url = "/api/me/"
        self.client.force_authenticate(user=self.base_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        url = "/api/me/"
        self.client.force_authenticate(user=self.base_user)
        payload = {"first_name": "Change"}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = self.base_user
        user.refresh_from_db()
        self.assertEqual(payload["first_name"], user.first_name)

    def test_change_password(self):
        url = "/api/password/password_reset/"
        self.client.force_authenticate(user=self.base_user)
        payload = {
            "current_password": self.user_data["password"],
            "new_password": "changepassword",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = self.base_user
        user.refresh_from_db()
        self.assertTrue(user.check_password(payload["new_password"]))

    def test_public_user(self):
        url = "/api/users/"
        self.client.force_authenticate(user=self.base_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
