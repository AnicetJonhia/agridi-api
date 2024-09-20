from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwnerOrReadOnly
from .models import Need
from .serializers import NeedSerializer

class NeedViewSet(viewsets.ModelViewSet):
    queryset = Need.objects.all()
    serializer_class = NeedSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
