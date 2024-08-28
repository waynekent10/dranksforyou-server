from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Ingredient, User
from dranksforyouapi.views.ingredients import IngredientSerializer

class IngredientTests(APITestCase):
    
    fixtures = ['ingredient', 'user']
    
    def setUp(self):
            self.user = User.objects.create (name='John Doe', email='john@example.com', username='johndoe', uid='12345')
            self.ingredient = Ingredient.objects.create(
            name="Lemon",
        )

    def test_create_ingredient(self):
        """Test creating an ingredient"""
        url = "/ingredients"
        ingredient = {
            "name": "Pepper"
        }

        response = self.client.post(url, ingredient, format='json')
        
        new_ingredient = Ingredient.objects.last()
        
        expected = IngredientSerializer(new_ingredient)
        
        self.assertEqual(expected.data, response.data)

     

    def test_get_ingredient(self):
        """Test retrieving a single ingredient"""
        ingredient = Ingredient.objects.first()
        
        url = f'/ingredients/{ingredient.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = IngredientSerializer(ingredient)
        self.assertEqual(expected.data, response.data)
   

    def test_list_ingredients(self):
        """Test list ingredients"""
        url = '/ingredients'

        response = self.client.get(url)
        
        # Get all the games in the database and serialize them to get the expected output
        all_ingredients = Ingredient.objects.all()
        expected = IngredientSerializer(all_ingredients, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_ingredient(self):
        """test update ingredient"""
   
        ingredient = Ingredient.objects.first()

        url = f'/ingredients/{ingredient.id}'

        updated_ingredient = {
            "name": f'{ingredient.name} updated',
        }

        response = self.client.put(url, updated_ingredient, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Refresh the game object to reflect any changes in the database
        ingredient.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_ingredient['name'], ingredient.name)

    def test_delete_ingredient(self):
        """Test delete game"""
        ingredient = Ingredient.objects.first()

        url = f'/ingredients/{ingredient.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
