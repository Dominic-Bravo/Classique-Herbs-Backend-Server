from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Order, OrderItem
from users.models import Customer
from catalog.models import Category, Product

# Model Tests
class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St'
        )

    def test_order_creation(self):
        order = Order.objects.create(
            customer=self.customer,
            total_amount=50.00,
            status='Pending'
        )
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.total_amount, 50.00)
        self.assertEqual(order.status, 'Pending')

    def test_order_str(self):
        order = Order.objects.create(
            customer=self.customer,
            total_amount=75.50,
            status='Processing'
        )
        self.assertEqual(str(order), f'Order {order.id} - John Doe')

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St'
        )
        self.category = Category.objects.create(
            category_name='Test Category',
            description='Test Description'
        )
        self.product = Product.objects.create(
            category=self.category,
            product_name='Test Product',
            description='Test Description',
            price=20.00,
            stock_quantity=10
        )
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=40.00,
            status='Pending'
        )

    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_purchase=20.00
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price_at_purchase, 20.00)

    def test_order_item_str(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price_at_purchase=20.00
        )
        self.assertEqual(str(order_item), f'{self.product.product_name} x 1')

# API Tests
class OrderAPITest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St'
        )
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=50.00,
            status='Pending'
        )

    def test_get_orders_list(self):
        response = self.client.get('/api/orders/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_order_detail(self):
        response = self.client.get(f'/api/orders/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Pending')

    def test_create_order(self):
        data = {
            'customer': self.customer.id,
            'total_amount': 75.00,
            'status': 'Processing'
        }
        response = self.client.post('/api/orders/orders/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_update_order(self):
        data = {
            'customer': self.customer.id,
            'total_amount': 60.00,
            'status': 'Shipped'
        }
        response = self.client.put(f'/api/orders/orders/{self.order.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Shipped')

    def test_delete_order(self):
        response = self.client.delete(f'/api/orders/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

class OrderItemAPITest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St'
        )
        self.category = Category.objects.create(
            category_name='Test Category',
            description='Test Description'
        )
        self.product = Product.objects.create(
            category=self.category,
            product_name='Test Product',
            description='Test Description',
            price=20.00,
            stock_quantity=10
        )
        self.order = Order.objects.create(
            customer=self.customer,
            total_amount=40.00,
            status='Pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_purchase=20.00
        )

    def test_get_order_items_list(self):
        response = self.client.get('/api/orders/order-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_order_item_detail(self):
        response = self.client.get(f'/api/orders/order-items/{self.order_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 2)

    def test_create_order_item(self):
        data = {
            'order': self.order.id,
            'product': self.product.id,
            'quantity': 1,
            'price_at_purchase': 20.00
        }
        response = self.client.post('/api/orders/order-items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_update_order_item(self):
        data = {
            'order': self.order.id,
            'product': self.product.id,
            'quantity': 3,
            'price_at_purchase': 20.00
        }
        response = self.client.put(f'/api/orders/order-items/{self.order_item.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, 3)

    def test_delete_order_item(self):
        response = self.client.delete(f'/api/orders/order-items/{self.order_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderItem.objects.count(), 0)

class CreateOrderAPITest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St'
        )
        self.category = Category.objects.create(
            category_name='Test Category',
            description='Test Description'
        )
        self.product1 = Product.objects.create(
            category=self.category,
            product_name='Product 1',
            description='Description 1',
            price=10.00,
            stock_quantity=20
        )
        self.product2 = Product.objects.create(
            category=self.category,
            product_name='Product 2',
            description='Description 2',
            price=15.00,
            stock_quantity=15
        )

    def test_create_order_success(self):
        data = {
            'customer_id': self.customer.id,
            'items': [
                {'product_id': self.product1.id, 'quantity': 2},
                {'product_id': self.product2.id, 'quantity': 1}
            ]
        }
        response = self.client.post('/api/orders/create-order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
        self.assertEqual(response.data['total_amount'], 35.00)  # (2*10) + (1*15)

        # Check order was created
        order = Order.objects.get(id=response.data['order_id'])
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.total_amount, 35.00)
        self.assertEqual(order.status, 'Pending')

        # Check order items
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(order_items.count(), 2)

        # Check stock was updated
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock_quantity, 18)  # 20 - 2
        self.assertEqual(self.product2.stock_quantity, 14)  # 15 - 1

    def test_create_order_insufficient_stock(self):
        data = {
            'customer_id': self.customer.id,
            'items': [
                {'product_id': self.product1.id, 'quantity': 25}  # More than available
            ]
        }
        response = self.client.post('/api/orders/create-order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Insufficient stock', response.data['error'])

        # Check no order was created
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_invalid_customer(self):
        data = {
            'customer_id': 999,  # Non-existent customer
            'items': [
                {'product_id': self.product1.id, 'quantity': 1}
            ]
        }
        response = self.client.post('/api/orders/create-order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Customer not found', response.data['error'])

    def test_create_order_invalid_product(self):
        data = {
            'customer_id': self.customer.id,
            'items': [
                {'product_id': 999, 'quantity': 1}  # Non-existent product
            ]
        }
        response = self.client.post('/api/orders/create-order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Product 999 not found', response.data['error'])

    def test_create_order_missing_data(self):
        # Missing customer_id
        data = {
            'items': [
                {'product_id': self.product1.id, 'quantity': 1}
            ]
        }
        response = self.client.post('/api/orders/create-order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Missing items
        data = {
            'customer_id': self.customer.id
        }
        response = self.client.post('/api/orders/create-order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
