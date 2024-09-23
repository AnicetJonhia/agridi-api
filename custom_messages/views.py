from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from core.permissions import IsMessageOwner, IsGroupOwnerOrMember
from .models import Message, Group
from .serializers import MessageSerializer, GroupSerializer


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

