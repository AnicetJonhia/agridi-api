# Generated by Django 4.2.16 on 2024-09-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_messages', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='messages/files/'),
        ),
    ]
