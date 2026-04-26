from rest_framework import viewsets, permissions
from api.models import Customer
from api.serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for Customers.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    # Example: restrict access to authenticated staff or the customer themselves
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure customers can only see their own profile.
        Staff can see all customers.
        """
        return Customer.objects.for_request(self.request)