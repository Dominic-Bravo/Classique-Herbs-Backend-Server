from django.db import models
from .customer import Customer
from .products import Product
from .base import BaseModel


class OrderQuerySet(models.QuerySet):
    def for_request(self, request):
        user = request.user
        if user.is_staff:
            return self.all()

        if user.is_authenticated:
            return self.filter(customer__email=user.email)

        psid = request.query_params.get('psid') or request.session.get('psid')
        if psid:
            return self.filter(customer__psid=psid)

        email = request.query_params.get('email')
        if email:
            return self.filter(customer__email=email)

        return self.none()


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def for_request(self, request):
        return self.get_queryset().for_request(request)


class Order(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    objects = OrderManager()

    def __str__(self):
        return f"Order {self.id} - {self.customer}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"