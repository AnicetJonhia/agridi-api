from django.contrib import admin

# Register your models here.
from .models import Group, Message, File

admin.site.register([Group, Message, File ])