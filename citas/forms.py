from django import forms
from .models import Servicio, Especialista


class SerEspForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "servicio" in self.data:
            servicio_id = int(self.data.get("servicio"))
            self.fields["especialista"].queryset = Especialista.objects.filter(
                especialidades__id=servicio_id
            )


class ClientInfoForm(forms.Form):
    nombre = forms.CharField(max_length=255)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=255)
