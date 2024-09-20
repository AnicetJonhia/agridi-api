from rest_framework import viewsets


from core.permissions import IsAdminUser
from .models import Stat
from .serializers import StatSerializer

class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_admin:
            return Stat.objects.all()

        return Stat.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        serializer.save(user_id=user_id)
