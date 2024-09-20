from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from core.permissions import IsAdminOrReadOnly
from .models import Season, Crop, Event
from .serializers import SeasonSerializer, CropSerializer, EventSerializer


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAdminOrReadOnly]
