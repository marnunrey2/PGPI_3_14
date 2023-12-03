# Generated by Django 4.2.7 on 2023-12-01 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('citas', '0014_alter_servicio_precio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reclamacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('cita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citas.cita')),
                ('invitado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reclamaciones', to='citas.invitado')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reclamaciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
