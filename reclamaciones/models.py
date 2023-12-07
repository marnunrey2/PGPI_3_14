from django.db import models
from django.conf import settings


class Reclamacion(models.Model):
    ABIERTO = "Abierto"
    CERRADO = "Cerrado"

    ESTADO_CHOICES = [
        (ABIERTO, "Abierto"),
        (CERRADO, "Cerrado"),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default=ABIERTO)
    cita = models.ForeignKey("citas.Cita", on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return f"{self.cita} - {self.estado}"
