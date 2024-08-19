from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dranksforyouapi.models import OrderBeverage, Beverage, Order


class OrderBeverageView(ViewSet):
    
    def retrieve(self, request, pk):
        try:
            order_beverage = OrderBeverage.objects.get(pk=pk)
            serializer = OrderBeverage(order_beverage)
            return Response(serializer.data)
        except order_beverage.DoesNotExist:
            return Response({'message': 'orderbeverage not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def list (self, request):
            order_beverages=OrderBeverage.objects.all()
            serializer = OrderBeverageSerializer(order_beverages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def create(self, request):
            order = Order.objects.get(pk=request.data["order_id"])
            beverage = Beverage.objects.get(pk=request.data['beverage_id'])
            
            order_beverage = OrderBeverage.objects.create(
                order= order,
                beverage = beverage
            )
            
            serializer = OrderBeverage(order_beverage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk):
            order_beverage = OrderBeverage.objects.get(pk=pk)
            order_beverage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class OrderBeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBeverage
        fields = ('id', 'order_id', 'beverage_id')
        depth = 1
            
