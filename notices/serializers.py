from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'news', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
