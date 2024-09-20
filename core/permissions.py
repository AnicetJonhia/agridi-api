from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """
    Permission qui permet aux administrateurs de créer, mettre à jour ou supprimer
    des objets, mais seulement aux utilisateurs authentifiés de les lire.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            # Permettre à tout le monde de lire
            return True
        return request.user and request.user.is_admin

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return   obj.user == request.user or request.user.is_admin


class IsMessageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user



class IsProducer(BasePermission):
    """
    Permission pour les producteurs uniquement.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Pro'

class IsCollector(BasePermission):
    """
    Permission pour les collecteurs uniquement.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Col'

class IsConsumer(BasePermission):
    """
    Permission pour les consommateurs uniquement.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Con'
