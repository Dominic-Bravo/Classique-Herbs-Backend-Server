from rest_framework import serializers
from api.models import Order, OrderItem
from .customer import CustomerSerializer # Import specifically what you need

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True) # Nested for clean API output

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'total_amount', 'items']