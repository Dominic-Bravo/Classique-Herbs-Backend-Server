from decimal import Decimal

from rest_framework import serializers
from api.models import Customer, Order, OrderItem
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

        customer = self._get_or_create_customer(customer_data)

        order = Order.objects.create(customer=customer, **validated_data)

        total_amount = Decimal('0')
        for item in items_data:
            order_item = OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_purchase=item['price_at_purchase'],
            )
            total_amount += order_item.price_at_purchase * order_item.quantity

        order.total_amount = total_amount
        order.save()
        return order

    def _get_or_create_customer(self, customer_data):
        psid = customer_data.get('psid')
        email = customer_data.get('email')

        if psid:
            customer, created = Customer.objects.get_or_create(psid=psid, defaults=customer_data)
            if not created:
                for attr, value in customer_data.items():
                    setattr(customer, attr, value)
                customer.save()
            return customer

        if email:
            customer, created = Customer.objects.get_or_create(email=email, defaults=customer_data)
            if not created:
                for attr, value in customer_data.items():
                    setattr(customer, attr, value)
                customer.save()
            return customer

        return Customer.objects.create(**customer_data)