from rest_framework import serializers

from orders.serializers import OrderSerializer
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    total_orders = serializers.ReadOnlyField()
    orders_details = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_orders_details(self, obj):
        request = self.context.get('request')
        if request and request.user == obj.user:
            orders = obj.orders.all()
            return OrderSerializer(orders, many=True).data
        return None