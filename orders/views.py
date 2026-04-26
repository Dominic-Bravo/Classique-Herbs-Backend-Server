from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order, OrderItem
from catalog.models import Product
from users.models import Customer
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class CreateOrderView(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customer_id')
        items = data.get('items')  # list of {'product_id': id, 'quantity': q}

        if not customer_id or not items:
            return Response({'error': 'customer_id and items are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            order = Order.objects.create(customer=customer, total_amount=0, status='Pending')
            total = 0
            for item in items:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                if not product_id or not quantity:
                    return Response({'error': 'Each item must have product_id and quantity'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    product = Product.objects.select_for_update().get(id=product_id)
                except Product.DoesNotExist:
                    return Response({'error': f'Product {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)
                if product.stock_quantity < quantity:
                    return Response({'error': f'Insufficient stock for {product.product_name}'}, status=status.HTTP_400_BAD_REQUEST)
                price = product.price
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price_at_purchase=price)
                total += price * quantity
                product.stock_quantity -= quantity
                product.save()
            order.total_amount = total
            order.save()

        return Response({'order_id': order.id, 'total_amount': total, 'status': 'Order created successfully'}, status=status.HTTP_201_CREATED)
