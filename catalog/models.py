from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'Categories'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'Products'
