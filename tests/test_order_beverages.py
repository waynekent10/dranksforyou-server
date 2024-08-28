from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import OrderBeverage
from dranksforyouapi.views.order_beverages import OrderBeverageSerializer

class OrderBeverageViewTests(APITestCase):

    def setUp(self):
        
        self.beverage =OrderBeverage.objects.first()

    def test_create_order_beverage(self):
        """Test creating  order beverage"""
        url = "/orderbeverages"
        orderbeverage = {
            "order_id": "2",
            "beverage_id": "1",
        }

        response = self.client.post(url, orderbeverage, format='json')
        
        new_beverage = OrderBeverage.objects.last()
        
        expected = OrderBeverageSerializer(new_beverage)
        
        self.assertEqual(expected.data, response.data)

    def test_get_order_beverage(self):
        """Test retrieving a single orderbeverage"""
        orderbeverage = OrderBeverage.objects.first()
        
        url = f'/orderbeverages/{orderbeverage.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = OrderBeverageSerializer(orderbeverage)
        self.assertEqual(expected.data, response.data)
        
    def test_list_beverage(self):
        """Test list orderbeverages"""
        url = '/orderbeverages'

        response = self.client.get(url)
        
       
        all_orderbeverages = OrderBeverage.objects.all()
        expected = OrderBeverageSerializer(all_orderbeverages, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)
        
    def test_change_beverage(self):
        """test update beverage"""
   
        orderbeverage = OrderBeverage.objects.first()

        url = f'/orderbeverages/{orderbeverage.id}'

        updated_orderbeverage = {
            "liquor_id": f'{orderbeverage.liquor_id} updated',
            "ingredient_id": orderbeverage.ingredient_id,
        }

        response = self.client.put(url, updated_orderbeverage, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    
        orderbeverage.refresh_from_db()

        self.assertEqual(updated_orderbeverage['liquor_id'], orderbeverage.liquor_id)


    def test_delete_beverage(self):
        """Test delete beverage"""
        orderbeverage = OrderBeverage.objects.first()

        url = f'/orderbeverages/{orderbeverage.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

 