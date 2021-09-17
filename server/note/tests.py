from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .models import Note

User = get_user_model()


class UserAuthTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "example@example.com",
            "username": "demousername",
            "password": "demopassword",
        }
        self.note_data = {
            "name": "Demo Note",
            "content": "Description Description Description Description ",
        }
        self.base_user = User.objects.create_user(**self.user_data)
        self.base_note = Note.objects.create(**self.note_data, owner=self.base_user)
        self.client = APIClient()

    def create_second_user(self):
        self.second_user = User.objects.create_user(
            **{
                "email": "change@email.com",
                "username": "change",
                "password": "demopassword",
            }
        )
        return self.second_user

    def share_note_with_base_user(self):
        self.second_note = Note.objects.create(
            **{
                "name": "Demo Note",
                "content": "Description Description Description Description ",
                "owner": self.create_second_user(),
            }
        )
        self.second_note.share_with.add(self.base_user.id)
        return self.second_note

    def test_note_create(self):
        url = "/api/note/"
        self.client.force_authenticate(user=self.base_user)
        payload = {
            "name": "Change",
            "content": "Description Description Description Description ",
            "tags": ["One", "Two"],
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_notes(self):
        url = "/api/note/"
        self.client.force_authenticate(user=self.base_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_details(self):
        note = Note.objects.filter(owner=self.base_user).first()
        url = f"/api/note/{note.slug}/"
        self.client.force_authenticate(user=self.base_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_update(self):
        note = Note.objects.filter(owner=self.base_user).first()
        url = f"/api/note/{note.slug}/"
        self.client.force_authenticate(user=self.base_user)
        payload = {"name": "Change"}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = self.base_note
        note.refresh_from_db()
        self.assertEqual(payload["name"], note.name)

    def test_delete_note(self):
        note = Note.objects.filter(owner=self.base_user).first()
        url = f"/api/note/{note.slug}/"
        self.client.force_authenticate(user=self.base_user)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_note_add_and_remove_user(self):
        note = Note.objects.filter(owner=self.base_user).first()
        self.client.force_authenticate(user=self.base_user)
        second_user = self.create_second_user()

        """Add Users with note"""
        url = f"/api/note/{note.slug}/add_user/"
        payload = {"users": [f"{second_user.username}"]}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        """Remove User with note"""
        url = f"/api/note/{note.slug}/remove_user/"
        payload = {"user": second_user.username}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_share_with_me_note(self):
        _ = self.share_note_with_base_user()
        url = "/api/share-note/"
        self.client.force_authenticate(user=self.base_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_share_with_me_note_details(self):
        shared_note = self.share_note_with_base_user()
        url = f"/api/share-note/{shared_note.slug}/"
        self.client.force_authenticate(user=self.base_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
