from .base import BaseModel
from django.db import models


class CustomerQuerySet(models.QuerySet):
    def for_request(self, request):
        user = request.user
        if user.is_staff:
            return self.all()

        if user.is_authenticated:
            return self.filter(email=user.email)

        return self.none()


class CustomerManager(models.Manager):
    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def for_request(self, request):
        return self.get_queryset().for_request(request)


class Customer(BaseModel):
    psid = models.CharField(max_length=100, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    objects = CustomerManager()

    def __str__(self):
        return self.psid or f"{self.name}"