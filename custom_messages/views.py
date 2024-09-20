from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import  IsMessageOwner
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user) | Message.objects.filter(sender=self.request.user)

