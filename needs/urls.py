from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NeedViewSet

router = DefaultRouter()
router.register(r'', NeedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
