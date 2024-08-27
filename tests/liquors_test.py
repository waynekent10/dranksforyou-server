from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Liquor

class LiquorViewTests(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.liquor = Liquor.objects.create(name="Whiskey")

    def test_retrieve_liquor(self):
        """Test retrieving a single liquor"""
        url = reverse('liquor-detail', args=[self.liquor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.liquor.name)

    def test_retrieve_liquor_not_found(self):
        """Test retrieving a non-existent liquor"""
        url = reverse('liquor-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_liquors(self):
        """Test listing all liquors"""
        url = reverse('liquor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.liquor.name)

    def test_create_liquor(self):
        """Test creating a new liquor"""
        url = reverse('liquor-list')
        data = {"name": "Vodka"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Vodka")

    def test_create_liquor_invalid(self):
        """Test creating a liquor with invalid data"""
        url = reverse('liquor-list')
        data = {"name": ""}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_liquor(self):
        """Test updating an existing liquor"""
        url = reverse('liquor-detail', args=[self.liquor.id])
        data = {"name": "Updated Whiskey"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Whiskey")

    def test_update_liquor_not_found(self):
        """Test updating a non-existent liquor"""
        url = reverse('liquor-detail', args=[999])
        data = {"name": "Non-existent Liquor"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_liquor(self):
        """Test deleting an existing liquor"""
        url = reverse('liquor-detail', args=[self.liquor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Liquor.objects.filter(pk=self.liquor.id).exists())

    def test_delete_liquor_not_found(self):
        """Test deleting a non-existent liquor"""
        url = reverse('liquor-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
