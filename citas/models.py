from datetime import datetime
from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="servicios", null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre


class Especialista(models.Model):
    nombre = models.CharField(max_length=255)
    especialidades = models.ManyToManyField("Servicio", related_name="especialistas")

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
    fecha = models.DateField()
    hora = models.TimeField()

    def clean(self):
        # Check if the selected servicio is offered by the chosen especialista
        if self.servicio not in self.especialista.especialidades.all():
            raise ValidationError("El servicio no es ofrecido por el especialista.")

        existing_appointments = Cita.objects.filter(
            especialista=self.especialista,
            fecha=self.fecha,
            hora=self.hora,
        ).exclude(
            pk=self.pk
        )  # Exclude the current appointment if it's an update
        if existing_appointments.exists():
            raise ValidationError(
                "Ya hay una cita programada con este especialista en este horario."
            )
        if type(self.fecha) == str:
            self.fecha = datetime.strptime(self.fecha, "%Y-%m-%d").date()

        if self.fecha < datetime.today().date() or (
            self.fecha == datetime.today().date() and self.hora < datetime.now().time()
        ):
            raise ValidationError("La fecha no puede ser anterior a la actual.")

    def save(self, *args, **kwargs):
        # Run the clean method before saving
        self.clean()
        super().save(*args, **kwargs)


@receiver(post_delete, sender=Cita)
def delete_invitado_if_no_citas(sender, instance, **kwargs):
    # Check if the deleted Cita's Invitado has no more citas
    if instance.invitado and instance.invitado.citas.count() == 0:
        instance.invitado.delete()

    def __str__(self):
        return f"Cita {self.pk} - {self.servicio.nombre} con {self.especialista.nombre} el {self.fecha}"
