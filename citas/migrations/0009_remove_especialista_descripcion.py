# Generated by Django 4.2.7 on 2023-11-19 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0008_especialista_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especialista',
            name='descripcion',
        ),
    ]
