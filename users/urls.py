from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileUpdateView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),

    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
]
