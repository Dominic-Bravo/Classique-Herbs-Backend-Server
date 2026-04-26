from rest_framework.routers import DefaultRouter
from api.views import product_views, order_views, customer_views

router = DefaultRouter()
router.register(r'categories', product_views.CategoryViewSet)
router.register(r'products', product_views.ProductViewSet)
router.register(r'orders', order_views.OrderViewSet)

urlpatterns = router.urls