from django.views import View
from django.http import JsonResponse
from orders.models import Order

class PaymentCallbackView(View):
    def post(self, request):
        data = request.POST
        transaction_id = data.get('transaction_id')
        status = data.get('status')  # État de la transaction envoyé par Mobile Money

        # Trouver la commande correspondante
        try:
            order = Order.objects.get(transaction_id=transaction_id)
            order.transaction_status = status
            order.save()
            return JsonResponse({'status': 'success'})
        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
