# users/management/commands/send_email.py

from django.core.management.base import BaseCommand
from sparkpost import SparkPost

class Command(BaseCommand):
    help = 'Send an email using SparkPost'

    def handle(self, *args, **kwargs):
        sp = SparkPost('6912aa60ad79a28972ff13c767f8abbdab21a310')  # Remplacez par votre clé API SparkPost
        try:
            response = sp.transmissions.send(
                recipients=['anicet22.aps2a@gmail.com'],
                html='<html><body><p>Ceci est un e-mail de test.</p></body></html>',
                subject='Sujet de Test',
                from_email='anicet.17aj@gmail.com',
            )
            self.stdout.write(self.style.SUCCESS('E-mail envoyé avec succès !'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de l\'envoi de l\'e-mail : {e}'))
