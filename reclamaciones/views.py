from datetime import date
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from .models import Reclamacion
from citas.models import Cita
from .forms import ReclamacionAddForm


class ReclamacionView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            reclamaciones = Reclamacion.objects.filter(cita__usuario=request.user)
            context = {"reclamaciones": reclamaciones}
            return render(request, "reclamaciones.html", context)
        else:
            return redirect("home:home")


class ReclamacionAddView(APIView):
    def post(self, request, cita_id):
        form = ReclamacionAddForm(request.POST)
        cita = get_object_or_404(Cita, pk=cita_id)
        if form.is_valid() and cita.usuario == request.user:
            mensaje = form.cleaned_data["mensaje"]
            Reclamacion.objects.create(
                cita=cita,
                mensaje=mensaje,
                fecha=date.today(),
            )
            return redirect("/reclamaciones")
        else:
            msg = "Error en el formulario"
            return render(request, "reclamacion_add.html", {"form": form, "msg": msg})

    def get(self, request, cita_id):
        if request.user.is_authenticated:
            cita = get_object_or_404(Cita, pk=cita_id)
            form = ReclamacionAddForm()
            return render(
                request, "reclamaciones_add.html", {"form": form, "cita": cita}
            )
        else:
            return redirect("home:home")
