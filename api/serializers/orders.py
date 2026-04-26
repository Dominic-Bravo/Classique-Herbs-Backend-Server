from rest_framework import serializers
from api.models import Order, OrderItem
from api.services.order_service import OrderService
from .customer import CustomerSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = CustomerSerializer()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'total_amount', 'items']
        read_only_fields = ['total_amount']

    def create(self, validated_data):
        customer_data = validated_data.pop('customer', None)
        items_data = validated_data.pop('items', [])

        if not customer_data:
            raise serializers.ValidationError({'customer': 'Customer information is required.'})

        return OrderService.create_order(validated_data, customer_data, items_data)


