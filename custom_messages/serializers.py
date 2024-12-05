
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Message, Group, File

User = get_user_model()
class UserSerializerForMessage(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id', 'username', 'email','profile_picture']

    def get_profile_picture(self, obj):

        if obj.profile_picture:
            return f"{self.context['request'].build_absolute_uri(obj.profile_picture.url)}"
        return None



class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializerForMessage(many=True, read_only=True)
    owner = UserSerializerForMessage(read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['owner']

    def get_photo(self, obj):

        if obj.photo:
            return f"{self.context['request'].build_absolute_uri(obj.photo.url)}"
        return None




class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_at']

class MessageSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    receiver = UserSerializerForMessage(read_only=True)
    sender = UserSerializerForMessage(read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'timestamp']