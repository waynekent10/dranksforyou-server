from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from dranksforyouapi.models import Liquor

class LiquorView(ViewSet):
    def retrieve(self,request, pk):
       liquor = Liquor.objects.get(pk=pk)
       serializer = LiquorSerializer(liquor, context={'request': request})
       return Response(serializer.data, status=status.HTTP_200_OK)
   
    def list(self, request): 
        liquors = Liquor.objects.all()
        serializer = LiquorSerializer(liquors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations"""
        liquor = Liquor.objects.create(
        name=request.data['name']
        )
        serializer = LiquorSerializer(liquor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     
    def update(self, request, pk):
        try:
            liquor = Liquor.objects.get(pk=pk)
        except Liquor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = LiquorSerializer(liquor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Handle DELETE requests to delete an order"""
        try:
            liquor = Liquor.objects.get(pk=pk)
            liquor.delete()
            return Response({'message': 'Liquor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Liquor.DoesNotExist:
            return Response({'message': 'Liquor not found'}, status=status.HTTP_404_NOT_FOUND)
   
class LiquorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liquor
        fields = ['id', 'name']
        depth = 2