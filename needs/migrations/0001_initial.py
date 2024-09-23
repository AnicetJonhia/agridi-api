# Generated by Django 4.2.16 on 2024-09-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Need',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('variety', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivery_deadline', models.DateField()),
            ],
        ),
    ]
