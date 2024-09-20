from django.db import models

from users.models import User


class Stat(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    is_admin_generated = models.BooleanField(default=False)