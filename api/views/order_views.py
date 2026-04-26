from rest_framework import permissions, viewsets
from api.models import Order
from api.serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.is_authenticated:
            return Order.objects.filter(customer__email=user.email)

        psid = self.request.query_params.get('psid') or self.request.session.get('psid')
        if psid:
            return Order.objects.filter(customer__psid=psid)

        email = self.request.query_params.get('email')
        if email:
            return Order.objects.filter(customer__email=email)

        return Order.objects.none()

    def perform_create(self, serializer):
        order = serializer.save()
        if not self.request.user.is_authenticated and order.customer.psid:
            self.request.session['psid'] = order.customer.psid
        return order