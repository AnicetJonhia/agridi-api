from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwnerOrReadOnly
from .models import Product

from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}
