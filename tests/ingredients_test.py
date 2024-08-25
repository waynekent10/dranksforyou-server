from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Ingredient

class IngredientViewTests(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.ingredient = Ingredient.objects.create(name="Lime")

    def test_retrieve_ingredient(self):
        """Test retrieving a single ingredient"""
        url = reverse('ingredient-detail', args=[self.ingredient.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.ingredient.name)

    def test_retrieve_ingredient_not_found(self):
        """Test retrieving a non-existent ingredient"""
        url = reverse('ingredient-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_ingredients(self):
        """Test listing all ingredients"""
        url = reverse('ingredient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.ingredient.name)

    def test_create_ingredient(self):
        """Test creating a new ingredient"""
        url = reverse('ingredient-list')
        data = {"name": "Mint"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Mint")

    def test_create_ingredient_invalid(self):
        """Test creating an ingredient with invalid data"""
        url = reverse('ingredient-list')
        data = {"name": ""}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ingredient(self):
        """Test updating an existing ingredient"""
        url = reverse('ingredient-detail', args=[self.ingredient.id])
        data = {"name": "Updated Lime"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Lime")

    def test_update_ingredient_not_found(self):
        """Test updating a non-existent ingredient"""
        url = reverse('ingredient-detail', args=[999])
        data = {"name": "Non-existent Ingredient"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_ingredient(self):
        """Test deleting an existing ingredient"""
        url = reverse('ingredient-detail', args=[self.ingredient.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ingredient.objects.filter(pk=self.ingredient.id).exists())

    def test_delete_ingredient_not_found(self):
        """Test deleting a non-existent ingredient"""
        url = reverse('ingredient-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
