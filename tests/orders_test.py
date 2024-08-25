from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Order, User

class OrderViewTests(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create(username="testuser", email="testuser@example.com", name="Test User", admin=False)
        self.order = Order.objects.create(user=self.user, order_total=50.00, payment_type="Credit Card")

    def test_retrieve_order(self):
        """Test retrieving a single order"""
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_total'], str(self.order.order_total))

    def test_retrieve_order_not_found(self):
        """Test retrieving a non-existent order"""
        url = reverse('order-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_orders(self):
        """Test listing all orders"""
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['order_total'], str(self.order.order_total))

    def test_create_order(self):
        """Test creating a new order"""
        url = reverse('order-list')
        data = {
            "user_id": self.user.id,
            "order_total": 75.00,
            "payment_type": "PayPal"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['order_total'], "75.00")

    def test_create_order_user_not_found(self):
        """Test creating an order with a non-existent user"""
        url = reverse('order-list')
        data = {
            "user_id": 999,  # Non-existent user ID
            "order_total": 75.00,
            "payment_type": "PayPal"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order(self):
        """Test updating an existing order"""
        url = reverse('order-detail', args=[self.order.id])
        data = {
            "user_id": self.user.id,
            "order_total": 100.00,
            "payment_type": "Debit Card"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_total'], "100.00")

    def test_update_order_not_found(self):
        """Test updating a non-existent order"""
        url = reverse('order-detail', args=[999])
        data = {
            "user_id": self.user.id,
            "order_total": 100.00,
            "payment_type": "Debit Card"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        """Test deleting an existing order"""
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.id).exists())

    def test_delete_order_not_found(self):
        """Test deleting a non-existent order"""
        url = reverse('order-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
