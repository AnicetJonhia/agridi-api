from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwnerOrReadOnly
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity_ordered = serializer.validated_data['quantity']

        if quantity_ordered > product.quantity:
            raise serializers.ValidationError("La quantité commandée dépasse le stock disponible.")


        order = serializer.save(user=self.request.user)

        product.decrease_quantity(quantity_ordered)
