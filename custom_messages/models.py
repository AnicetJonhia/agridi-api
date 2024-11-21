from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='member_groups')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    photo = models.ImageField(upload_to='custom_messages/group_photos/', blank=True, null=True)


    def __str__(self):
        return self.name

    def clean(self):
        if self.members.count() < 2:
            raise ValidationError('A group must have at least two members apart from the owner.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class File(models.Model):
    file = models.FileField(upload_to='custom_messages/files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class Message(models.Model):
    content = models.TextField(blank=True, null=True)
    files = models.ManyToManyField(File, related_name='messages', blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.group:
            return f'Message in {self.group.name} from {self.sender} at {self.timestamp}'
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'


