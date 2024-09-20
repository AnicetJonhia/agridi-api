from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Need

class NeedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Need
        fields = '__all__'
        read_only_fields = ['user']
