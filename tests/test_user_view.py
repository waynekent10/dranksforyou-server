from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import User

class UserViewTests(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="testuser@example.com",
            admin=False,
            uid="unique-id-1234"
        )

    def test_retrieve_user(self):
        """Test retrieving a single user"""
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_retrieve_user_not_found(self):
        """Test retrieving a non-existent user"""
        url = reverse('user-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_users(self):
        """Test listing all users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], self.user.username)

    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list')
        data = {
            "name": "New User",
            "username": "newuser",
            "email": "newuser@example.com",
            "admin": True,
            "uid": "unique-id-5678"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], "newuser")

    def test_update_user(self):
        """Test updating an existing user"""
        url = reverse('user-detail', args=[self.user.id])
        data = {
            "name": "Updated User",
            "username": "updateduser",
            "email": "updateduser@example.com",
            "admin": True,
            "uid": "unique-id-9101"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "updateduser")

    def test_update_user_not_found(self):
        """Test updating a non-existent user"""
        url = reverse('user-detail', args=[999])
        data = {
            "name": "Updated User",
            "username": "updateduser",
            "email": "updateduser@example.com",
            "admin": True,
            "uid": "unique-id-9101"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        """Test deleting an existing user"""
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.id).exists())

    def test_delete_user_not_found(self):
        """Test deleting a non-existent user"""
        url = reverse('user-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
