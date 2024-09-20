from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet

router = DefaultRouter()
router.register(r'notices', NoticeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
