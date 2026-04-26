from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer

# Model Tests
class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St, City, State 12345'
        )
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.last_name, 'Doe')
        self.assertEqual(customer.email, 'john.doe@example.com')
        self.assertEqual(customer.phone, '123-456-7890')
        self.assertEqual(customer.address, '123 Main St, City, State 12345')

    def test_customer_str(self):
        customer = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='098-765-4321',
            address='456 Oak Ave, Town, State 67890'
        )
        self.assertEqual(str(customer), 'Jane Smith')

    def test_customer_email_unique(self):
        Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St'
        )
        with self.assertRaises(Exception):  # Should raise IntegrityError
            Customer.objects.create(
                first_name='Johnny',
                last_name='Doe',
                email='john.doe@example.com',  # Duplicate email
                phone='123-456-7891',
                address='124 Main St'
            )

# API Tests
class CustomerAPITest(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St, City, State 12345'
        )

    def test_get_customers_list(self):
        response = self.client.get('/api/users/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_get_customer_detail(self):
        response = self.client.get(f'/api/users/customers/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john.doe@example.com')

    def test_create_customer(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '098-765-4321',
            'address': '456 Oak Ave, Town, State 67890'
        }
        response = self.client.post('/api/users/customers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_update_customer(self):
        data = {
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'email': 'johnny.doe@example.com',
            'phone': '123-456-7890',
            'address': '123 Main St, City, State 12345'
        }
        response = self.client.put(f'/api/users/customers/{self.customer.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'Johnny')
        self.assertEqual(self.customer.email, 'johnny.doe@example.com')

    def test_delete_customer(self):
        response = self.client.delete(f'/api/users/customers/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)
