from rest_framework import serializers
from .models import Order, OrderItem
from users.models import Customer
from catalog.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)  # or use ProductSerializer

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'