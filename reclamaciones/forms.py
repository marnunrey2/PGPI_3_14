from django import forms


class ReclamacionAddForm(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea)
