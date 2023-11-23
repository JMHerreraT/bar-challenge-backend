# urls.py
from rest_framework.routers import DefaultRouter
from .views import BeerViewSet, OrderViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'beers', BeerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = router.urls
