from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Beverage
from dranksforyouapi.views.beverages import BeverageSerializer

class BeverageViewTests(APITestCase):

    def setUp(self):
        
        self.beverage =Beverage.objects.first()

    def test_create_beverage(self):
        """Test creating a beverage"""
        url = "/beverages"
        beverage = {
            "name": "Peach",
            "liquor_id": "2",
            "ingredient_id": "3",
            "description": "a drink to be had",
            "price": 10.00
        }

        response = self.client.post(url, beverage, format='json')
        
        new_beverage = Beverage.objects.last()
        
        expected = BeverageSerializer(new_beverage)
        
        self.assertEqual(expected.data, response.data)

    def test_get_beverage(self):
        """Test retrieving a single beverage"""
        beverage = Beverage.objects.first()
        
        url = f'/beverages/{beverage.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = BeverageSerializer(beverage)
        self.assertEqual(expected.data, response.data)
        
    def test_list_beverage(self):
        """Test list beverages"""
        url = '/beverages'

        response = self.client.get(url)
        
       
        all_beverages = Beverage.objects.all()
        expected = BeverageSerializer(all_beverages, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)
        
    def test_change_beverage(self):
        """test update beverage"""
   
        beverage = Beverage.objects.first()

        url = f'/beverages/{beverage.id}'

        updated_beverage = {
            "name": f'{beverage.name} updated',
            "liquor_id": beverage.liquor_id,
            "ingredient_id": beverage.ingredient_id,
            "description": beverage.description,
            "price": beverage.price,
        }

        response = self.client.put(url, updated_beverage, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    
        beverage.refresh_from_db()

        self.assertEqual(updated_beverage['name'], beverage.name)


    def test_delete_beverage(self):
        """Test delete beverage"""
        beverage = Beverage.objects.first()

        url = f'/beverages/{beverage.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

 