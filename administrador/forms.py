from django import forms
from citas.models import Servicio, Especialista, Invitado
from citas.utils import calculate_available_hours
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CitaServicioAddForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "id": "usuario_select"}),
    )
    invitado = forms.ModelChoiceField(
        queryset=Invitado.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "id": "invitado_select"}),
    )
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

    def __init__(self, *args, **kwargs):
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

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        invitado = cleaned_data.get("invitado")

        if usuario and invitado:
            raise ValidationError(
                "Both usuario and invitado cannot be filled. Please choose only one."
            )

        return cleaned_data


class CitaEspecialistaAddForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "id": "usuario_select"}),
    )
    invitado = forms.ModelChoiceField(
        queryset=Invitado.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "id": "invitado_select"}),
    )
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

    def __init__(self, *args, **kwargs):
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

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        invitado = cleaned_data.get("invitado")

        if usuario and invitado:
            raise ValidationError(
                "Both usuario and invitado cannot be filled. Please choose only one."
            )

        return cleaned_data


class ServicioAddForm(forms.Form):
    nombre = forms.CharField(max_length=255)
    descripcion = forms.CharField(widget=forms.Textarea)
    imagen = forms.ImageField(required=False)
    precioId = forms.CharField(max_length=255)


class EspecialistaAddForm(forms.Form):
    nombre = forms.CharField(max_length=255)
    imagen = forms.ImageField(required=False)

    especialidades = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )


class ReclamacionAddForm(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea)


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


class InvitadoAddForm(forms.Form):
    nombre = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=254, required=True)
