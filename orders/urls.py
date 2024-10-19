from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,  CreateOrderView

router = DefaultRouter()
router.register(r'', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('/create/<int:product_id>/', CreateOrderView.as_view(), name='create_order'),
]





