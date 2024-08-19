from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dranksforyouapi.models import Ingredient

class IngredientView(ViewSet):
    def retrieve(self,request, pk):
       ingredient = Ingredient.objects.get(pk=pk)
       serializer = IngredientSerializer(ingredient, context={'request': request})
       return Response(serializer.data, status=status.HTTP_200_OK)
   
    def list(self, request): 
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations"""
        ingredient = Ingredient.objects.create(
        name=['name']
        )
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     
    def update(self, request, pk):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = IngredientSerializer(ingredient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete an order"""
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredient.delete()
            return Response({'message': 'Ingredient deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Ingredient.DoesNotExist:
            return Response({'message': 'Ingredient not found'}, status=status.HTTP_404_NOT_FOUND)
   
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        depth = 1