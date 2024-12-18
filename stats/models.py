from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Stat(models.Model):
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)
    description = models.TextField(blank=True, null=True)
    is_admin_generated = models.BooleanField(default=False)