from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import User, Beverage, Order, OrderBeverage
from dranksforyouapi.views.order_beverages import OrderBeverageSerializer

class OrderBeverageViewTestCase(APITestCase):

    def setUp(self):
        # Create necessary data for User, Beverage, and Order
        self.user = User.objects.create(
            name='John Doe',
            email='john@example.com',
            username='johndoe',
            uid='12345'
        )
        
        self.beverage = Beverage.objects.create(
            name="Peach",
            liquor_id="123",
            ingredient_id="456",
            description="A slurpy",
            price=10.00
        )
        
        self.order = Order.objects.create(
            user=self.user,
            order_total=10.00,
            payment_type='Cash'
        )
        
        self.order_beverage = OrderBeverage.objects.create(
            order=self.order,
            beverage=self.beverage
        )

    def test_list_order_beverages(self):
        """Test listing all order beverages"""
        url = reverse('orderbeverage-list')
        response = self.client.get(url)

        order_beverages = OrderBeverage.objects.all()
        serializer = OrderBeverageSerializer(order_beverages, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_order_beverage(self):
        """Test retrieving a single order beverage"""
        url = reverse('orderbeverage-detail', args=[self.order_beverage.id])
        response = self.client.get(url)

        serializer = OrderBeverageSerializer(self.order_beverage)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_order_beverage(self):
        """Test creating a new order beverage"""
        url = reverse('orderbeverage-list')
        data = {
            'order': self.order.id,
            'beverage': self.beverage.id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderBeverage.objects.count(), 2)  # Should have 2 order_beverages now

    def test_destroy_order_beverage(self):
        """Test deleting an order beverage"""
        url = reverse('orderbeverage-detail', args=[self.order_beverage.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderBeverage.objects.count(), 0)  # Should be no order_beverages now
