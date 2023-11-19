from django.shortcuts import render, get_object_or_404
from .forms import ServicioEspecialistaForm
from rest_framework.views import APIView
from citas.models import Servicio, Especialista


class ReservaView(APIView):
    def post(self, request):
        form = ServicioEspecialistaForm(request.POST)

        if form.is_valid():
            servicio = form.cleaned_data.get("servicio")
            especialista = form.cleaned_data.get("especialista")
            form.save()
            return render(
                request,
                "calendario.html",
                {"servicio": servicio, "especialista": especialista},
            )
        else:
            msg = "Error en el formulario"
            return render(request, "reserva.html", {"form": form, "msg": msg})

    def get(self, request):
        servicios = Servicio.objects.all()
        especialistas = Especialista.objects.all()
        form = ServicioEspecialistaForm(None)
        return render(
            request,
            "reserva.html",
            {"form": form, "servicios": servicios, "especialistas": especialistas},
        )


class GetCalendarioView(APIView):
    def post(self, request):
        servicio = request.data.get("servicio")
        especialista = request.data.get("especialista")
        return render(
            request,
            "calendario.html",
            {"servicio": servicio, "especialista": especialista},
        )
