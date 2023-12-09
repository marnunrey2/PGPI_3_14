from django import forms
from .models import Servicio, Especialista, Invitado
from django.contrib.auth.models import User
from .utils import calculate_available_hours
from django.shortcuts import get_object_or_404


class CitaServicioAddForm(forms.Form):
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
        widget=forms.RadioSelect(
            attrs={"class": "payment-method"},
        ),
        initial="EF",
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        servicio = kwargs.pop("servicio", None)
        initial_especialista = kwargs.pop("initial_especialista", None)

        super().__init__(*args, **kwargs)
        if servicio:
            self.servicio = servicio
            self.fields["especialista"].queryset = Especialista.objects.filter(
                especialidades=servicio
            )

        if initial_especialista is not None:
            self.initial["especialista"] = initial_especialista
        else:
            self.initial["especialista"] = None

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
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.none(),
        widget=forms.Select(
            attrs={
                "hx-target": "#id_especialista",
                "class": "service-select",
            }
        ),
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
    metodo_pago = forms.ChoiceField(
        choices=(("EF", "Efectivo"), ("TA", "Tarjeta")),
        widget=forms.RadioSelect(
            attrs={"class": "payment-method"},
        ),
        initial="EF",
    )

    nombre = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        especialista = kwargs.pop("especialista", None)
        initial_servicio = kwargs.pop("initial_servicio", None)

        super().__init__(*args, **kwargs)
        if especialista:
            self.especialista = especialista
            especialista_id = especialista.id
            print(especialista_id)
            self.fields["servicio"].queryset = Servicio.objects.filter(
                especialistas=especialista_id
            )

        if initial_servicio is not None:
            self.initial["servicio"] = initial_servicio
        else:
            self.initial["servicio"] = None

        print(especialista_id)

        if "fecha" in self.data and especialista:
            fecha = self.data.get("fecha")
            print(especialista_id)
            available_hours = [
                (hour, hour)
                for hour in calculate_available_hours(fecha, especialista_id)
            ]
            self.fields["hora"].choices = available_hours

        if user and user.is_authenticated:
            del self.fields["nombre"]
            del self.fields["email"]
            del self.fields["telefono"]
