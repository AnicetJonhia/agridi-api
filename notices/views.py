from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwnerOrReadOnly
from .models import Notice
from .serializers import NoticeSerializer

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
