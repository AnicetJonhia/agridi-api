from rest_framework import serializers
from .models import Season, Crop, Event


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    crops = CropSerializer(many=True, read_only=True)
    events = EventSerializer(many=True, read_only=True)
    class Meta:
        model = Season
        fields = '__all__'

