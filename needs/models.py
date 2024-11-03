from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Need(models.Model):
    product_name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_deadline = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
