from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = "Hacher les mots de passe des utilisateurs qui ne sont pas encore hachés"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:

            if not user.password.startswith('pbkdf2_sha256$'):
                user.set_password(user.password)
                user.save()

