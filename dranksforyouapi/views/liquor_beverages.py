from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dranksforyouapi.models import LiquorBeverage, Beverage, Liquor


class LiquorBeverageView(ViewSet):
    
    def retrieve(self, request, pk):
        try:
            liquor_beverage = LiquorBeverage.objects.get(pk=pk)
            serializer = LiquorBeverageSerializer(liquor_beverage)
            return Response(serializer.data)
        except LiquorBeverage.DoesNotExist:
            return Response({'message': 'liquor beverage not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def list (self, request):
            liquor_beverages=LiquorBeverage.objects.all()
            serializer = LiquorBeverageSerializer(liquor_beverages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def create(self, request):
            liquor = Liquor.objects.get(pk=request.data["liquor"])
            beverage = Beverage.objects.get(pk=request.data['beverage'])
            
            liquor_beverage = LiquorBeverage.objects.create(
                liquor= liquor,
                beverage = beverage
            )
            
            serializer = LiquorBeverageSerializer(liquor_beverage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
        try:
            liquor_beverage = LiquorBeverage.objects.get(pk=pk)
            liquor_beverage.delete()
            return Response({'message': 'liquorBeverage deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except LiquorBeverage.DoesNotExist:
            return Response({'message': 'liquorBeverage not found'}, status=status.HTTP_404_NOT_FOUND)
        
class LiquorBeverageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LiquorBeverage
        fields = ('id', 'liquor', 'beverage')
        depth = 1
            
