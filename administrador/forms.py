from django import forms
from citas.models import Servicio, Especialista
from citas.utils import calculate_available_hours
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


"""
class CitaAddForm(forms.Form):
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.Select(
            attrs={
                "hx-get": "/especialistas_opciones/",
                "hx-target": "#id_especialista",
            }
        ),
    )
    especialista = forms.ModelChoiceField(
        queryset=Especialista.objects.none(),
    )
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "hx-get": "/horas_disponibles/",
                "hx-include": "#id_especialista",
                "hx-target": "#id_hora",
                "placeholder": "YYYY-mm-dd",
                "pattern": "\d{4}-\d{2}-\d{2}",
            }
        )
    )
    hora = forms.ChoiceField(choices=[])

    nombre = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if "servicio" in self.data:
            servicio_id = int(self.data.get("servicio"))
            self.fields["especialista"].queryset = Especialista.objects.filter(
                especialidades__id=servicio_id
            )
        if "fecha" in self.data and "especialista" in self.data:
            fecha = self.data.get("fecha")
            especialista_id = int(self.data.get("especialista"))
            available_hours = [
                (hour, hour)
                for hour in calculate_available_hours(fecha, especialista_id)
            ]
            self.fields["hora"].choices = available_hours
"""


class ServicioAddForm(forms.Form):
    nombre = forms.CharField(max_length=255)
    descripcion = forms.CharField(widget=forms.Textarea)
    imagen = forms.ImageField(required=False)
    precio = forms.DecimalField(max_digits=10, decimal_places=2)


class EspecialistaAddForm(forms.Form):
    nombre = forms.CharField(max_length=255)
    especialidades = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )


class UsuarioAddForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
