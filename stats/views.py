from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Stat
from .serializers import StatSerializer

class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Stat.objects.all()

        return Stat.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
