# Generated by Django 4.2.7 on 2023-11-19 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0005_cita_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='especialista',
            name='descripcion',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
