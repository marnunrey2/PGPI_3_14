# Generated by Django 4.2.7 on 2023-12-10 18:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("citas", "0003_precita"),
    ]

    operations = [
        migrations.AddField(
            model_name="especialista",
            name="agotado",
            field=models.BooleanField(default=False),
        ),
    ]
