from django import forms
from .models import Servicio, Especialista, Invitado
from django.contrib.auth.models import User
from .utils import calculate_available_hours
from django.shortcuts import get_object_or_404


class CitaServicioAddCarritoForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        servicio = kwargs.pop("servicio", None)

        super().__init__(*args, **kwargs)

        if servicio:
            self.fields["especialista"].queryset = Especialista.objects.filter(
                especialidades__id=servicio.id
            )

        if "fecha" in self.data and "especialista" in self.data:
            fecha = self.data.get("fecha")
            especialista_id = int(self.data.get("especialista"))
            available_hours = [
                (hour, hour)
                for hour in calculate_available_hours(fecha, especialista_id)
            ]
            self.fields["hora"].choices = available_hours


class CitaEspecialistaAddCarritoForm(forms.Form):
    especialista = forms.CharField(widget=forms.HiddenInput(), label="", required=False)
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

    def __init__(self, *args, **kwargs):
        especialista = kwargs.pop("especialista", None)

        super().__init__(*args, **kwargs)

        if especialista:
            self.fields["especialista"].initial = especialista.id
            self.fields["servicio"].queryset = Servicio.objects.filter(
                especialistas=especialista.id
            )

        if "fecha" in self.data and especialista:
            fecha = self.data.get("fecha")
            available_hours = [
                (hour, hour)
                for hour in calculate_available_hours(fecha, especialista.id)
            ]
            self.fields["hora"].choices = available_hours
