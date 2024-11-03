

from django.db import models

from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    negotiated_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending')

    # Champs pour la transaction
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    transaction_status = models.CharField(max_length=50, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='Mobile Money')  # ou tout autre méthode

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return self.quantity * self.negotiated_price

    def __str__(self):
        return f"Order #{self.id} | {self.quantity} x {self.product.name} | Status: {self.status} | Transaction Status: {self.transaction_status} | By {self.user.username}"

