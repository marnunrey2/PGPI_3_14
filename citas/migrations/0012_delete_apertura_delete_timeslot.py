# Generated by Django 4.2.7 on 2023-11-21 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0011_apertura'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Apertura',
        ),
        migrations.DeleteModel(
            name='TimeSlot',
        ),
    ]
