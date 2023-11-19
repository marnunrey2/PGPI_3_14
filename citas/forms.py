from django import forms
from .models import Servicio, Especialista


class ServicioEspecialistaForm(forms.Form):
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all(), empty_label=None)
    especialista = forms.ModelChoiceField(
        queryset=Especialista.objects.none(), empty_label=None, required=False
    )

    def init(self, servicio, args, **kwargs):
        super().init(args, **kwargs)
        self.fields["especialista"].queryset = servicio.especialidades.all()


class ClientInfoForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=255)
    # Add more fields if required
