from django.db import models
from django.conf import settings

class Notice(models.Model):
    news = models.ForeignKey('news.News', related_name='notices', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notice by {self.user} on {self.news}'
