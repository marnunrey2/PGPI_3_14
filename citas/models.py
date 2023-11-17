from django.db import models

from django.conf import settings


class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="servicios", null=True, blank=True)


class Especialista(models.Model):
    nombre = models.CharField(max_length=255)
    especialidades = models.ManyToManyField("Servicio", related_name="especialistas")


class Invitado(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=255)


class Cita(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="citas",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    invitado = models.ForeignKey(
        "Invitado",
        related_name="citas",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    servicio = models.ForeignKey("Servicio", on_delete=models.CASCADE)
    especialista = models.ForeignKey("Especialista", on_delete=models.CASCADE)
    fecha = models.DateTimeField()
