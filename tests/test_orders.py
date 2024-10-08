from rest_framework import status
from rest_framework.test import APITestCase
from dranksforyouapi.models import Order, User
from dranksforyouapi.views.orders import OrderSerializer

class OrderTests(APITestCase):
    
    fixtures = ['user', 'order']
    
    def setUp(self):
        self.user = User.objects.create (name='John Doe', email='john@example.com', username='johndoe', uid='12345')
        self.order = Order.objects.create(
            user=self.user,
            order_total=10.00,
            payment_type='cash'
        )


    def test_create_order(self):
        """Test creating an order"""
        url = "/orders"
        order = {
            "user_id": self.user.id,
            "order_total": 150.00,
            "payment_type": "cash"
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

    def test_update_order(self):
        """test update order"""
   
        order = Order.objects.first()

        url = f'/orders/{self.order.id}'

        updated_order = {
            "user_id": self.user.id,
            "order_total": 10.00,
            "payment_type": order.payment_type,
        }

        response = self.client.put(url, updated_order, format='json')

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

        # Refresh the game object to reflect any changes in the database
        order.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_order['order_total'], self.order.order_total)
        self.assertEqual(updated_order['payment_type'], self.order.payment_type)

    def test_delete_order(self):
        """Test delete order"""
        order = Order.objects.first()

        url = f'/orders/{order.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)


        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
