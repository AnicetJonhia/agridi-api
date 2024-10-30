from rest_framework import serializers
from users.models import User
from .models import Message, Group

class UserSerializerForMessage(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id', 'username', 'email','profile_picture']

    def get_profile_picture(self, obj):

        if obj.profile_picture:
            return f"{self.context['request'].build_absolute_uri(obj.profile_picture.url)}"
        return None



class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['owner']

    def get_photo(self, obj):

        if obj.photo:
            return f"{self.context['request'].build_absolute_uri(obj.photo.url)}"
        return None

class MessageSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    receiver = UserSerializerForMessage(read_only=True)
    sender = UserSerializerForMessage(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'timestamp']

    def get_file(self, obj):

            if obj.file:
                return f"{self.context['request'].build_absolute_uri(obj.file.url)}"
            return None
