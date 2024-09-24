from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, GroupViewSet

router = DefaultRouter()

router.register(r'groups', GroupViewSet)
router.register(r'', MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
