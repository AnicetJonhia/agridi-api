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
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    alternate_email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

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