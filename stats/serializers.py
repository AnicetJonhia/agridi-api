from rest_framework import serializers
from .models import Stat

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }