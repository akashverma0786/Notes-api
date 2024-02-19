from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Note, noteHistory

class SignupTestCase(APITestCase):
    def test_signup(self):
        """
        Test to ensure we can create a new user account.
        """
        url = reverse('signup')
        data = {'username': 'testuser', 'password': 'password123', 'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login(self):
        """
        Test to ensure we can log a user in and receive a token.
        """
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)


class CreateNoteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        """
        Test to ensure we can create a new note.
        """
        url = reverse('create_note')
        data = {'title': 'Test Note', 'content': 'This is a test note.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Note')


class ShareNoteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(title='Test Note', content='This is a test note.', owner=self.user)

    def test_share_note(self):
        """
        Test to ensure we can share a note with another user.
        """
        url = reverse('share_note')
        data = {'note_id': self.note.id, 'users': ['otheruser']}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Note shared successfully')


class GetNoteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(title='Test Note', content='This is a test note.', owner=self.user)

    def test_get_note(self):
        """
        Test to ensure we can retrieve a note by id.
        """
        url = reverse('get_note', args=[self.note.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Note')
        self.assertEqual(response.data['content'], 'This is a test note.')


class UpdateNoteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(title='Test Note', content='Original Content', owner=self.user)

    def test_update_note(self):
        """
        Test to ensure we can update an existing note.
        """
        url = reverse('update_note', args=[self.note.id])
        data = {'title': 'Updated Test Note', 'content': 'Updated Content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Test Note')
        self.assertEqual(self.note.content, 'Updated Content')


class GetNoteVersionHistoryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.note = Note.objects.create(title='Test Note', content='Original Content', owner=self.user)
        # updating the note to create a history entry
        self.note.content = 'Updated Content'
        self.note.save()
        noteHistory.objects.create(note=self.note, content='Original Content')

    def test_get_note_version_history(self):
        """
        Test to ensure we can retrieve the version history of a note.
        """
        url = reverse('get_note_version_history', args=[self.note.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]['content'], 'Original Content')