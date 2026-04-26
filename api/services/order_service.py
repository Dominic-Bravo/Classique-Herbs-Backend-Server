from decimal import Decimal

from api.models import Order, OrderItem
from api.services.customer_service import CustomerService


class OrderService:
    @staticmethod
    def create_order(order_data, customer_data, items_data):
        if not customer_data:
            raise ValueError('Customer information is required.')

        customer = CustomerService.get_or_create_customer(customer_data)
        order = Order.objects.create(customer=customer, **order_data)

        total_amount = Decimal('0')
        for item_data in items_data:
            total_amount += OrderService._create_order_item(order, item_data)

        order.total_amount = total_amount
        order.save(update_fields=['total_amount'])
        return order

    @staticmethod
    def _create_order_item(order, item_data):
        order_item = OrderItem.objects.create(order=order, **item_data)
        return order_item.price_at_purchase * order_item.quantity

    @staticmethod
    def attach_psid_to_session(order, request):
        if not request.user.is_authenticated and order.customer.psid:
            request.session['psid'] = order.customer.psid
