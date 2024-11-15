from django.db import models
from core.permissions import IsMessageOwner, IsGroupOwnerOrMember
from django.db.models import Max, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message, Group, File
from .serializers import MessageSerializer, GroupSerializer, FileSerializer
from users.models import User
from rest_framework.parsers import MultiPartParser
import logging

logger = logging.getLogger(__name__)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsGroupOwnerOrMember]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
       
        user = self.request.user
        return Group.objects.filter(members=user).distinct()

    def perform_create(self, serializer):
        group = serializer.save(owner=self.request.user)
        members = self.request.data.getlist('members')
        group.members.set(members)
        group.save()

    def update(self, request, *args, **kwargs):
        group = self.get_object()

        if request.user == group.owner:
            return super().update(request, *args, **kwargs)

        elif request.user in group.members.all():
            serializer = self.get_serializer(group, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                allowed_fields = ['name', 'photo']
                if any(field not in allowed_fields for field in serializer.validated_data.keys()):
                    return Response({"detail": "Vous ne pouvez mettre à jour que le nom et la photo du groupe."},
                                    status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data)
        return Response({"detail": "Vous n'avez pas la permission de modifier ce groupe."},
                        status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def leave(self, request, pk=None):
        """Permet à l'utilisateur de quitter le groupe"""
        try:
            group = self.get_object()
        except Group.DoesNotExist:
            return Response({"detail": "Groupe non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        if request.user in group.members.all():
            group.members.remove(request.user)
            return Response({"detail": "Vous avez quitté le groupe."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Vous n'êtes pas membre de ce groupe."}, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageOwner]

    def perform_create(self, serializer):
        group = serializer.validated_data.get('group', None)
        if group:
            serializer.save(sender=self.request.user, group=group)
        else:
            serializer.save(sender=self.request.user)

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(receiver=self.request.user) | models.Q(sender=self.request.user) |
            models.Q(group__members=self.request.user)
        ).distinct()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], name='Conversations')
    def conversations(self, request):
        """Retourne la liste des dernières conversations avec le dernier message de chaque utilisateur ou groupe."""
        last_messages = (
            Message.objects
            .filter(
                Q(receiver=request.user) |
                Q(sender=request.user) |
                Q(group__members=request.user)
            )
            .annotate(last_message_id=Max('id'))

        )

        unique_conversations = {}
        for message in last_messages:
            if message.group:
                key = f"group_{message.group.id}"
            else:
                participants = sorted([message.sender.id, message.receiver.id])
                key = f"user_{participants[0]}_{participants[1]}"

            if key not in unique_conversations or unique_conversations[key].id < message.id:
                unique_conversations[key] = message

        unique_messages = unique_conversations.values()
        serializer = MessageSerializer(unique_messages, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def chat_history(self, request, pk=None, type=None):
        """Retourne l'historique des messages entre deux utilisateurs ou pour un groupe spécifique."""
        if type == 'private':
            try:
                receiver = User.objects.get(pk=pk)
                messages = Message.objects.filter(
                    models.Q(sender=request.user, receiver=receiver) |
                    models.Q(sender=receiver, receiver=request.user)
                ).order_by('timestamp')
                if not messages.exists():
                    logger.debug(f"No messages found between users {request.user.id} and {receiver.id}")
                serializer = MessageSerializer(messages, many=True, context={'request': request})
                return Response(serializer.data)
            except User.DoesNotExist:
                logger.debug(f"User with id {pk} does not exist")
                return Response({"detail": "Aucun utilisateur correspondant trouvé."},
                                status=status.HTTP_404_NOT_FOUND)
        elif type == 'group':
            try:
                group = Group.objects.get(pk=pk)
                messages = Message.objects.filter(group=group).order_by('timestamp')
                if not messages.exists():
                    logger.debug(f"No messages found for group {group.id}")
                serializer = MessageSerializer(messages, many=True, context={'request': request})
                return Response(serializer.data)
            except Group.DoesNotExist:
                logger.debug(f"Group with id {pk} does not exist")
                return Response({"detail": "Aucun groupe correspondant trouvé."},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Type invalide. Utilisez 'user' ou 'group'."},
                            status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], parser_classes=[MultiPartParser])
    def send_message(self, request):
        """Envoie un message à un utilisateur ou un groupe."""
        serializer = MessageSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            receiver_id = request.data.get('receiver', None)
            group_id = request.data.get('group', None)

            if receiver_id is None and group_id is None:
                return Response({"detail": "Vous devez spécifier soit un destinataire (receiver), soit un groupe."},
                                status=status.HTTP_400_BAD_REQUEST)

            receiver = None
            group = None

            if receiver_id is not None:
                try:
                    receiver = User.objects.get(pk=receiver_id)
                except User.DoesNotExist:
                    return Response({"detail": "Destinataire non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            if group_id is not None:
                try:
                    group = Group.objects.get(pk=group_id)
                except Group.DoesNotExist:
                    return Response({"detail": "Groupe non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            message = serializer.save(sender=request.user, receiver=receiver, group=group)

            # Handle file uploads
            files = request.FILES.getlist('files')
            for file in files:
                file_instance = File.objects.create(file=file)
                message.files.add(file_instance)

            return Response(MessageSerializer(message, context={'request': request}).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_file(self, request, pk=None, file_id=None):
        """Remove a file from a message's files."""
        try:
            message = self.get_object()
            file = message.files.get(pk=file_id)
            message.files.remove(file)
            file.delete()
            return Response({"detail": "File removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        except File.DoesNotExist:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)