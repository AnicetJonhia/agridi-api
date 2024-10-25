from rest_framework import serializers
from users.models import User
from .models import Message, Group

class UserSerializerForMessage(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['owner']

class MessageSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)
    receiver = UserSerializerForMessage(read_only=True)
    sender = UserSerializerForMessage(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'timestamp', 'receiver']
