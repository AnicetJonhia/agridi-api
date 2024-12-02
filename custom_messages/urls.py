from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:type>/<int:pk>/chat_history/', MessageViewSet.as_view({'get': 'chat_history'}), name='message-chat-history'),
    path('send_message/', MessageViewSet.as_view({'post': 'send_message'}), name='message-send'),
    path('<int:pk>/remove_file/<int:file_id>/', MessageViewSet.as_view({'delete': 'remove_file'}),
         name='message-remove-file'),
    path('<str:type>/<int:pk>/delete_conversation/', MessageViewSet.as_view({'delete': 'delete_conversation'}),
         name='delete_conversation'),
    path('groups/<int:pk>/add_member/', GroupViewSet.as_view({'post': 'add_member'}), name='group-add-member'),
    path('groups/<int:pk>/remove_member/', GroupViewSet.as_view({'post': 'remove_member'}), name='group-remove-member'),

    path('groups/<int:pk>/leave/', GroupViewSet.as_view({'post': 'leave'}), name='group-leave'),
]