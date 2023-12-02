from django.db import models
from django.conf import settings


class Reclamacion(models.Model):
    cita = models.ForeignKey("citas.Cita", on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateField()
