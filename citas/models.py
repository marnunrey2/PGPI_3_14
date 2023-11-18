from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError


class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="servicios", null=True, blank=True)

    def __str__(self):
        return self.nombre


class Especialista(models.Model):
    nombre = models.CharField(max_length=255)
    especialidades = models.ManyToManyField("Servicio", related_name="especialistas")
    # si quiero saber los servicios de un especialista: especialista.servicio_set.all()

    def __str__(self):
        return self.nombre


class Invitado(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


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

    def clean(self):
        # Check if the selected servicio is offered by the chosen especialista
        if self.servicio not in self.especialista.especialidades.all():
            raise ValidationError("El servicio no es ofrecido por el especialista.")

    def save(self, *args, **kwargs):
        # Run the clean method before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cita {self.pk} - {self.servicio.nombre} con {self.especialista.nombre} el {self.fecha}"