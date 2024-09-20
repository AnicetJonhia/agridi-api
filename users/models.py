from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Pro', 'Producteur'),
        ('Col', 'Collecteur'),
        ('Con', 'Consommateur'),
        ('Admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Ajoutez ces lignes pour résoudre les conflits
    groups = models.ManyToManyField(Group, related_name='users')
    user_permissions = models.ManyToManyField(Permission, related_name='users')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'Admin' or self.is_superuser

    @property
    def is_producer(self):
        return self.role == 'Pro'

    @property
    def is_collector(self):
        return self.role == 'Col'

    @property
    def is_consumer(self):
        return self.role == 'Con'

    def save(self, *args, **kwargs):

        if  self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)