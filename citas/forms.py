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

        if user and user.is_authenticated:
            del self.fields["nombre"]
            del self.fields["email"]
            del self.fields["telefono"]


class CitaEspecialistaAddForm(forms.Form):
    especialista = forms.CharField(widget=forms.HiddenInput(), label="")
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

        if user and user.is_authenticated:
            del self.fields["nombre"]
            del self.fields["email"]
            del self.fields["telefono"]
