from datetime import datetime
from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Servicio(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="servicios", null=True, blank=True)
    precioId = models.TextField(default="")
    agotado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Especialista(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to="especialistas", null=True, blank=True)
    especialidades = models.ManyToManyField("Servicio", related_name="especialistas")
    agotado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Invitado(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class PreCita(models.Model):
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

    def __str__(self):
        return f"Cita {self.pk} - {self.servicio.nombre} con {self.especialista.nombre}"


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

    class MetodoPago(models.TextChoices):
        EFECTIVO = "EF", "Efectivo"
        TARJETA = "TA", "Tarjeta"

    servicio = models.ForeignKey("Servicio", on_delete=models.CASCADE)
    especialista = models.ForeignKey("Especialista", on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    metodo_pago = models.CharField(
        max_length=2,
        choices=MetodoPago.choices,
        default=MetodoPago.EFECTIVO,
    )
    pagado = models.BooleanField()
    check_pago = models.CharField(max_length=255, null=True, blank=True)

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

    def __str__(self):
        return f"Cita {self.pk} - {self.servicio.nombre} con {self.especialista.nombre}"


@receiver(pre_delete, sender=Cita)
def delete_invitado_if_last_cita(sender, instance, **kwargs):
    # Check if the deleted instance is the last Cita associated with the Invitado
    invitado = instance.invitado
    if invitado and invitado.citas.count() == 1:
        # Disconnect the signal temporarily to avoid recursion
        pre_delete.disconnect(delete_invitado_if_last_cita, sender=Cita)
        invitado.delete()
        # Reconnect the signal after deletion
        pre_delete.connect(delete_invitado_if_last_cita, sender=Cita)
