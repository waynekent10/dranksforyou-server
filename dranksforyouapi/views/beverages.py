from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dranksforyouapi.models import Beverage

class BeverageView(ViewSet):
    def retrieve(self,request, pk):
       beverage = Beverage.objects.get(pk=pk)
       serializer = BeverageSerializer(Beverage, context={'request': request})
       return Response(serializer.data, status=status.HTTP_200_OK)
   
    def list(self, request): 
       beverages = Beverage.objects.all()
       serializer = BeverageSerializer(beverages, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        
        """Handle POST requests to create a new beverage"""
        beverage = Beverage.objects.create(
            beverage_name=request.data["name"],
            liquor_id=request.data["liquor_id"],
            ingredients=request.data["ingredients"],
            description=request.data["description"],
            price=request.data["price"]
        )
        serializer = BeverageSerializer(beverage)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   
    def destroy(self, request, pk):
        """Handle DELETE requests to delete an order"""
        try:
            beverage = Beverage.objects.get(pk=pk)
            beverage.delete()
            return Response({'message': 'Part deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Beverage.DoesNotExist:
            return Response({'message': 'Part not found'}, status=status.HTTP_404_NOT_FOUND)  
   
class BeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beverage
        fields = ['id', 'beverage_name', 'ingredient', 'description', 'price']
        depth = 2