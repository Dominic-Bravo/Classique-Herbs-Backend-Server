from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Product

# Model Tests
class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(
            category_name='Test Category',
            description='Test Description'
        )
        self.assertEqual(category.category_name, 'Test Category')
        self.assertEqual(category.description, 'Test Description')
        self.assertEqual(str(category), 'Test Category')  # Assuming __str__ method

    def test_category_str(self):
        category = Category.objects.create(
            category_name='Herbal Teas',
            description='Various herbal teas'
        )
        self.assertEqual(str(category), 'Herbal Teas')

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category',
            description='Test Description'
        )

    def test_product_creation(self):
        product = Product.objects.create(
            category=self.category,
            product_name='Test Product',
            description='Test Product Description',
            price=25.99,
            stock_quantity=50
        )
        self.assertEqual(product.product_name, 'Test Product')
        self.assertEqual(product.price, 25.99)
        self.assertEqual(product.stock_quantity, 50)
        self.assertEqual(product.category, self.category)

    def test_product_str(self):
        product = Product.objects.create(
            category=self.category,
            product_name='Green Tea',
            description='Healthy green tea',
            price=15.00,
            stock_quantity=100
        )
        self.assertEqual(str(product), 'Green Tea')

# API Tests
class CategoryAPITest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category',
            description='Test Description'
        )

    def test_get_categories_list(self):
        response = self.client.get('/api/catalog/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category_name'], 'Test Category')

    def test_get_category_detail(self):
        response = self.client.get(f'/api/catalog/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category_name'], 'Test Category')

    def test_create_category(self):
        data = {
            'category_name': 'New Category',
            'description': 'New Description'
        }
        response = self.client.post('/api/catalog/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=response.data['id']).category_name, 'New Category')

    def test_update_category(self):
        data = {
            'category_name': 'Updated Category',
            'description': 'Updated Description'
        }
        response = self.client.put(f'/api/catalog/categories/{self.category.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.category_name, 'Updated Category')

    def test_delete_category(self):
        response = self.client.delete(f'/api/catalog/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

class ProductAPITest(APITestCase):
    def setUp(self):
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

    def test_get_products_list(self):
        response = self.client.get('/api/catalog/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product_name'], 'Test Product')

    def test_get_product_detail(self):
        response = self.client.get(f'/api/catalog/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], 'Test Product')
        self.assertEqual(response.data['category']['category_name'], 'Test Category')

    def test_create_product(self):
        data = {
            'category': self.category.id,
            'product_name': 'New Product',
            'description': 'New Description',
            'price': 30.00,
            'stock_quantity': 25
        }
        response = self.client.post('/api/catalog/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product(self):
        data = {
            'category': self.category.id,
            'product_name': 'Updated Product',
            'description': 'Updated Description',
            'price': 25.00,
            'stock_quantity': 15
        }
        response = self.client.put(f'/api/catalog/products/{self.product.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.product_name, 'Updated Product')
        self.assertEqual(self.product.price, 25.00)

    def test_delete_product(self):
        response = self.client.delete(f'/api/catalog/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
