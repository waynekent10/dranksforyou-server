from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Beverage

class BeverageViewTests(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.beverage = Beverage.objects.create(
            name="Margarita",
            liquor_id="1",
            ingredient_id="1,2,3",
            description="A classic cocktail",
            price=9.99
        )

    def test_retrieve_beverage(self):
        """Test retrieving a single beverage"""
        url = reverse('beverage-detail', args=[self.beverage.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.beverage.name)

    def test_retrieve_beverage_not_found(self):
        """Test retrieving a non-existent beverage"""
        url = reverse('beverage-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_beverages(self):
        """Test listing all beverages"""
        url = reverse('beverage-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.beverage.name)

    def test_create_beverage(self):
        """Test creating a new beverage"""
        url = reverse('beverage-list')
        data = {
            "name": "Martini",
            "liquor_id": "2",
            "ingredient_id": "4,5,6",
            "description": "A sophisticated cocktail",
            "price": 12.50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Martini")

    def test_create_beverage_invalid(self):
        """Test creating a beverage with invalid data"""
        url = reverse('beverage-list')
        data = {
            "name": "",
            "liquor_id": "2",
            "ingredient_id": "4,5,6",
            "description": "A cocktail with no name",
            "price": 12.50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_beverage(self):
        """Test updating an existing beverage"""
        url = reverse('beverage-detail', args=[self.beverage.id])
        data = {
            "name": "Updated Margarita",
            "price": 10.99
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Margarita")
        self.assertEqual(float(response.data['price']), 10.99)

    def test_update_beverage_not_found(self):
        """Test updating a non-existent beverage"""
        url = reverse('beverage-detail', args=[999])
        data = {
            "name": "Non-existent Beverage",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_beverage(self):
        """Test deleting an existing beverage"""
        url = reverse('beverage-detail', args=[self.beverage.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Beverage.objects.filter(pk=self.beverage.id).exists())

    def test_delete_beverage_not_found(self):
        """Test deleting a non-existent beverage"""
        url = reverse('beverage-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
