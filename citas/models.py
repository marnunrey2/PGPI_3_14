from datetime import datetime
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

        cita_date = datetime.strptime(self.fecha, "%Y-%m-%d").date()

        if cita_date < datetime.today().date() or (
            cita_date == datetime.today().date() and self.hora < datetime.now().time()
        ):
            raise ValidationError("La fecha no puede ser anterior a la actual.")

    def save(self, *args, **kwargs):
        # Run the clean method before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cita {self.pk} - {self.servicio.nombre} con {self.especialista.nombre} el {self.fecha}"


class TimeSlot(models.Model):
    specialist = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    service = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # Other timeslot details

    def __str__(self):
        return f"{self.specialist.name} - {self.service.name} - {self.date} - {self.start_time} to {self.end_time}"


class Apertura(models.Model):
    dia = models.CharField(
        choices=(
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miercoles", "Miercoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
            ("Sabado", "Sabado"),
            ("Domingo", "Domingo"),
        ),
        max_length=10,
    )
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
