from django import forms


class TramitarReservaForm(forms.Form):
    metodo_pago = forms.ChoiceField(
        choices=(("EF", "Efectivo"), ("TA", "Tarjeta")),
        widget=forms.RadioSelect(
            attrs={"class": "payment-method"},
        ),
        initial="EF",
    )

    nombre = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            del self.fields["nombre"]
            del self.fields["email"]
