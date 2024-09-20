from rest_framework import viewsets

from core.permissions import  IsAdminOrReadOnly
from .models import News
from .serializers import NewsSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True)
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly]
