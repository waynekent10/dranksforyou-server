from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Order, User
from dranksforyouapi.views.orders import OrderSerializer

class OrderTests(APITestCase):
    
    fixtures = ['user', 'order']
    
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            username="testuser",
            email="testuser@example.com",
            uid="testuid"
        )

        # Create a test order
        self.order = Order.objects.create(
            user=self.user,
            order_total=50.00,
            payment_type="Credit Card"
        )

    def test_create_order(self):
        """Test creating an order"""
        url = "/orders"
        order = {
            "user_id": self.user.id,
            "order_total": 150.00,
            "payment_type": "PayPal"
        }

        response = self.client.post(url, order, format='json')
        
        new_order = Order.objects.last()
        
        expected = OrderSerializer(new_order)
        
        self.assertEqual(expected.data, response.data)

     

    def test_get_order(self):
        """Test retrieving a single order"""
        order = Order.objects.first()
        
        url = f'/orders/{order.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = OrderSerializer(order)
        self.assertEqual(expected.data, response.data)
   

    def test_list_orders(self):
        """Test list orders"""
        url = '/orders'

        response = self.client.get(url)
        
     
        all_orders = Order.objects.all()
        expected = OrderSerializer(all_orders, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_order(self):
        """test update order"""
   
        order = Order.objects.first()

        url = f'/orders/{order.id}'

        updated_order = {
            "order_total": f'{order.order_total} updated',
            "payment_type": order.payment_type,
        }

        response = self.client.put(url, updated_order, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Refresh the game object to reflect any changes in the database
        order.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_order['order_total'], order.order_total)

    def test_delete_order(self):
        """Test delete order"""
        order = Order.objects.first()

        url = f'/orders/{order.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
