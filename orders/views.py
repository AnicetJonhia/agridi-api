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

        # Appeler la fonction pour traiter le paiement ici
        transaction_id, transaction_status = self.process_payment(order)

        # Mettre à jour la commande avec les détails de la transaction
        order.transaction_id = transaction_id
        order.transaction_status = transaction_status
        order.save()

    def process_payment(self, order):
        # Logique pour le traitement de paiement avec Mobile Money
        transaction_id = "TRANSACTION12345"  # Exemple
        transaction_status = "completed"  # ou "failed", en fonction du résultat du paiement

        # Implémenter la logique d'appel API pour Mobile Money et gérer les erreurs

        return transaction_id, transaction_status
