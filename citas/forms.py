from django import forms
from .models import Servicio, Especialista, Invitado
from django.contrib.auth.models import User
from .utils import calculate_available_hours


class CitaServicioAddForm(forms.Form):
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.Select(
            attrs={
                "hx-get": "/especialistas_opciones/",
                "hx-target": "#id_especialista",
                "class": "service-select",
            }
        ),
    )
    especialista = forms.ModelChoiceField(
        queryset=Especialista.objects.none(),
    )
    fecha = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "hx-get": "/horas_disponibles/",
                "hx-include": "#id_especialista",
                "hx-target": "#id_hora",
            },
        ),
        input_formats=["%Y-%m-%d"],
    )
    hora = forms.ChoiceField(choices=[])

    nombre = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=20, required=False)
    metodo_pago = forms.ChoiceField(
        choices=(("EF", "Efectivo"), ("TA", "Tarjeta")),
        widget=forms.RadioSelect(attrs={"class": "payment-method"},),
        initial="EF",
    )

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

        if user and user.is_authenticated:
            del self.fields["nombre"]
            del self.fields["email"]
            del self.fields["telefono"]


class CitaEspecialistaAddForm(forms.Form):
    especialista = forms.ModelChoiceField(
        queryset=Especialista.objects.all(),
        widget=forms.Select(
            attrs={
                "hx-get": "/servicios_opciones/",
                "hx-target": "#id_servicio",
            }
        ),
    )
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.none(),
    )
    fecha = forms.DateField(
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "hx-get": "/horas_disponibles/",
                "hx-include": "#id_especialista",
                "hx-target": "#id_hora",
            },
        ),
        input_formats=["%Y-%m-%d"],
    )
    hora = forms.ChoiceField(choices=[])

    nombre = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if "especialista" in self.data:
            especialista_id = int(self.data.get("especialista"))
            self.fields["servicio"].queryset = Servicio.objects.filter(
                especialistas=especialista_id
            )
        if "fecha" in self.data and "especialista" in self.data:
            fecha = self.data.get("fecha")
            especialista_id = int(self.data.get("especialista"))
            available_hours = [
                (hour, hour)
                for hour in calculate_available_hours(fecha, especialista_id)
            ]
            self.fields["hora"].choices = available_hours

        if user and user.is_authenticated:
            del self.fields["nombre"]
            del self.fields["email"]
            del self.fields["telefono"]
