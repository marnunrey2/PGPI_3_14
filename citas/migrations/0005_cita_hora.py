# Generated by Django 4.2.7 on 2023-11-19 10:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0004_alter_cita_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='hora',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]