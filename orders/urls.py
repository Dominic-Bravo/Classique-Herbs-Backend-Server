from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
]