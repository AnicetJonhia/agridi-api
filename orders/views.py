from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsOwnerOrReadOnly
from .models import Order
from .serializers import OrderSerializer


from django.shortcuts import  redirect
from django.views import View

from products.models import Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



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





@method_decorator(login_required, name='dispatch')
class CreateOrderView(View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        quantity = int(request.POST.get('quantity'))
        negotiated_price = product.price  # Ou tout autre logique pour le prix

        # Créer une nouvelle commande
        order = Order.objects.create(
            product=product,
            user=request.user,
            quantity=quantity,
            negotiated_price=negotiated_price
        )

        # Appeler la fonction pour traiter le paiement ici
        transaction_id, transaction_status = self.process_payment(order)

        # Mettre à jour la commande avec les détails de la transaction
        order.transaction_id = transaction_id
        order.transaction_status = transaction_status
        order.save()

        return redirect('order_success', order_id=order.id)

    def process_payment(self, order):
        # Cette fonction doit intégrer votre logique de traitement de paiement avec Mobile Money
        # Ceci est un exemple fictif
        # Vous pouvez utiliser l'API de Mobile Money ici pour effectuer la transaction
        transaction_id = "TRANSACTION12345"  # Exemple
        transaction_status = "completed"  # ou "failed", en fonction du résultat du paiement

        # Implémenter la logique d'appel API pour Mobile Money et gérer les erreurs

        return transaction_id, transaction_status
