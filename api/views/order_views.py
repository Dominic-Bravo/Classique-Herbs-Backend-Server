from rest_framework import permissions, viewsets
from api.models import Order
from api.serializers import OrderSerializer
from api.services.order_service import OrderService


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.for_request(self.request)

    def perform_create(self, serializer):
        order = serializer.save()
        OrderService.attach_psid_to_session(order, self.request)
        return order