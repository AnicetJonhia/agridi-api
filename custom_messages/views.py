from django.db import models


from core.permissions import IsMessageOwner, IsGroupOwnerOrMember

from django.db.models import Max
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message, Group
from .serializers import MessageSerializer, GroupSerializer
from users.models import User

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsGroupOwnerOrMember]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        group = self.get_object()

        if request.user == group.owner:
            return super().update(request, *args, **kwargs)

        elif request.user in group.members.all():

            serializer = self.get_serializer(group, data=request.data, partial=True)
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
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], name='Conversations')
    def conversations(self, request):
        """Retourne la liste des dernières conversations avec le dernier message de chaque utilisateur ou groupe."""
        last_messages = (
            Message.objects
            .filter(models.Q(receiver=request.user) | models.Q(sender=request.user) | models.Q(group__members=request.user))
            .values('receiver', 'group')
            .annotate(last_message_id=Max('id'))
        )
        messages = Message.objects.filter(id__in=[item['last_message_id'] for item in last_messages])
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def chat_history(self, request, pk=None):
        """Retourne l'historique des messages entre deux utilisateurs ou pour un groupe spécifique."""
        try:
            group = Group.objects.get(pk=pk)
            messages = Message.objects.filter(group=group).order_by('timestamp')
        except Group.DoesNotExist:
            try:
                receiver = User.objects.get(pk=pk)
                messages = Message.objects.filter(
                    models.Q(sender=request.user, receiver=receiver) |
                    models.Q(sender=receiver, receiver=request.user)
                ).order_by('timestamp')
            except User.DoesNotExist:
                return Response({"detail": "Aucun utilisateur ou groupe correspondant trouvé."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)



