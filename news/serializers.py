from rest_framework import serializers

from notices.serializers import NoticeSerializer
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    notices = NoticeSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = '__all__'
