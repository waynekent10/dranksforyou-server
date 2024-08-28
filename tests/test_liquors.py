from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Liquor
from dranksforyouapi.views.liquors import LiquorSerializer

class LiquorViewTests(APITestCase):
    fixtures = ['liquor']
    
    def setUp(self):
        self.liquor = Liquor.objects.first()

    def test_create_liquor(self):
        """Test creating a liquor"""
        url = "/liquors"
        liquor = {
            "name": "Sake"
        }

        response = self.client.post(url, liquor, format='json')
        
        new_liquor = Liquor.objects.last()
        
        expected = LiquorSerializer(new_liquor)
        
        self.assertEqual(expected.data, response.data)

     

    def test_get_liquor(self):
        """Test retrieving a single liquor"""
        liquor = Liquor.objects.first()
        
        url = f'/liquors/{liquor.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = LiquorSerializer(liquor)
        self.assertEqual(expected.data, response.data)
   

    def test_list_liquors(self):
        """Test list liquors"""
        url = '/liquors'

        response = self.client.get(url)
        
       
        all_liquors = Liquor.objects.all()
        expected = LiquorSerializer(all_liquors, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_liquor(self):
        """test update liquor"""
   
        liquor = Liquor.objects.first()

        url = f'/liquors/{liquor.id}'

        updated_liquor = {
            "name": f'{liquor.name} updated',
        }

        response = self.client.put(url, updated_liquor, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    
        liquor.refresh_from_db()

        self.assertEqual(updated_liquor['name'], liquor.name)

    def test_delete_liquor(self):
        """Test delete game"""
        liquor = Liquor.objects.first()

        url = f'/liquors/{liquor.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
