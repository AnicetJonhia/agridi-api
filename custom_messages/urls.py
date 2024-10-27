from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/chat_history/', MessageViewSet.as_view({'get': 'chat_history'}), name='message-chat-history'),
    path('groups/<int:pk>/leave/', GroupViewSet.as_view({'post': 'leave'}), name='group-leave'),
]
