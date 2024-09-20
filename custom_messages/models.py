from django.db import models
from users.models import User

class Message(models.Model):
    content = models.TextField()
    file = models.FileField(upload_to='messages/files/', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'