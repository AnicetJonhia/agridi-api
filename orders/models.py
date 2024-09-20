from django.db import models
from users.models import User
from products.models import Product

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    negotiated_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='pending')


    def __str__(self):
        return f"Order of {self.quantity} {self.product.name} by {self.user}"