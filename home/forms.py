from django import forms


class SearchForm(forms.Form):
    servicio = forms.CharField(required=False)
    especialista = forms.CharField(required=False)
    max_precio = forms.DecimalField(
        required=False, min_value=0, max_digits=10, decimal_places=2
    )
