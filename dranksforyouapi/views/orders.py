from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dranksforyouapi.models import Order, User

class OrderView(ViewSet):
    def retrieve(self,request, pk):
       Order = Order.objects.get(pk=pk)
       serializer = OrderSerializer(Order, context={'request': request})
       return Response(serializer.data, status=status.HTTP_200_OK)
  
    def list(self, request): 
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations"""
        try:

            user = User.objects.get(pk=request.data['user_id'])
            
            order = Order.objects.create(
                user_id=user,
                order_total=request.data['order_total'],
                payment_type=request.data['payment_type']
            )
            
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            

    
    def destroy(self, request, pk):
        """Handle DELETE requests to delete an order"""
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({'message': 'Oder deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
  
  
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_total', 'payment_type']
        depth = 2