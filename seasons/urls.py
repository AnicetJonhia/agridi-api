from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeasonViewSet, CropViewSet, EventViewSet

router = DefaultRouter()
router.register(r'crops', CropViewSet)
router.register(r'events', EventViewSet)
router.register(r'', SeasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
