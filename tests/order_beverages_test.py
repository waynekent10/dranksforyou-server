from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import OrderBeverage, Beverage, Order, User

class OrderBeverageViewTests(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(username="testuser", email="testuser@example.com", name="Test User", admin=False)
        self.order = Order.objects.create(user=self.user, order_total=50.00, payment_type="Credit Card")
        self.beverage = Beverage.objects.create(name="Coke")
        self.order_beverage = OrderBeverage.objects.create(order_id=self.order, beverage_id=self.beverage)

    def test_retrieve_order_beverage(self):
        """Test retrieving a single order beverage"""
        url = reverse('orderbeverage-detail', args=[self.order_beverage.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_id'], self.order.id)
        self.assertEqual(response.data['beverage_id'], self.beverage.id)

    def test_retrieve_order_beverage_not_found(self):
        """Test retrieving a non-existent order beverage"""
        url = reverse('orderbeverage-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_order_beverages(self):
        """Test listing all order beverages"""
        url = reverse('orderbeverage-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['order_id'], self.order.id)

    def test_create_order_beverage(self):
        """Test creating a new order beverage"""
        url = reverse('orderbeverage-list')
        data = {
            "order_id": self.order.id,
            "beverage_id": self.beverage.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['order_id'], self.order.id)
        self.assertEqual(response.data['beverage_id'], self.beverage.id)

    def test_create_order_beverage_invalid_order(self):
        """Test creating an order beverage with an invalid order"""
        url = reverse('orderbeverage-list')
        data = {
            "order_id": 999,  # Non-existent order ID
            "beverage_id": self.beverage.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_order_beverage_invalid_beverage(self):
        """Test creating an order beverage with an invalid beverage"""
        url = reverse('orderbeverage-list')
        data = {
            "order_id": self.order.id,
            "beverage_id": 999  # Non-existent beverage ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_beverage(self):
        """Test deleting an existing order beverage"""
        url = reverse('orderbeverage-detail', args=[self.order_beverage.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(OrderBeverage.objects.filter(pk=self.order_beverage.id).exists())

    def test_delete_order_beverage_not_found(self):
        """Test deleting a non-existent order beverage"""
        url = reverse('orderbeverage-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
