from django.db import models

from notices.models import Notice


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_active = models.BooleanField(default=True)  # Gérer la visibilité de l'actualité


    # Champs pour les médias
    image = models.ImageField(upload_to='news/news_images/', blank=True, null=True)
    video = models.FileField(upload_to='news/news_videos/', blank=True, null=True)
    document = models.FileField(upload_to='news/news_documents/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


