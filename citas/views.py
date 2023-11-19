from django.shortcuts import render, redirect
from .forms import ServicioEspecialistaForm
from rest_framework.views import APIView
from citas.models import Servicio, Especialista


class ReservaView(APIView):
    def post(self, request):
        form = ServicioEspecialistaForm(request.POST)
        return render(
            request,
            "calendario.html",
            {"form": form},
        )
        """
        if form.is_valid():
            servicio = form.cleaned_data.get("servicio")
            especialista = form.cleaned_data.get("especialista")
            print(servicio)
            print(especialista)
            return render(
                request,
                "calendario.html",
                {"form": form, "servicio": servicio, "especialista": especialista},
            )
        else:
            msg = "Error en el formulario"
            return render(request, "reserva.html", {"form": form, "msg": msg})
        """

    def get(self, request):
        servicios = Servicio.objects.all()
        especialistas = Especialista.objects.all()
        form = ServicioEspecialistaForm(None)
        return render(
            request,
            "reserva.html",
            {"form": form, "servicios": servicios, "especialistas": especialistas},
        )


class CalendarioView(APIView):
    def get(self, request):
        return render(request, "calendario.html")
