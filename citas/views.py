from django.shortcuts import render, redirect
from .forms import CitaForm
from rest_framework.views import APIView
from citas.models import Servicio, Especialista, Invitado, Cita
from django.http import JsonResponse
from datetime import datetime, timedelta
from .utils import calculate_available_hours
from django.contrib.auth.models import User
from datetime import datetime


class CitaView(APIView):
    def post(self, request):
        form = CitaForm(request.POST)
        if form.is_valid():
            servicio_id = form.cleaned_data["servicio"].id
            especialista_id = form.cleaned_data["especialista"].id
            fecha = form.cleaned_data["fecha"].strftime("%Y-%m-%d")
            hora = form.cleaned_data["hora"]

            usuario = request.user if request.user.is_authenticated else None
            invitado = None

            if usuario is None:
                nombre = form.cleaned_data["nombre"]
                email = form.cleaned_data["email"]
                telefono = form.cleaned_data["telefono"]

                invitado = Invitado.objects.create(
                    nombre=nombre, email=email, telefono=telefono
                )

            cita = Cita.objects.create(
                usuario=usuario,
                invitado=invitado,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
            )
            return render(request, "home/home.html", {"cita": cita})

        else:
            msg = "Error en el formulario"
            return render(request, "crear_cita.html", {"form": form, "msg": msg})

    def get(self, request):
        form = CitaForm(user=request.user)
        return render(
            request,
            "crear_cita.html",
            {"form": form},
        )


def get_especialistas_por_servicio(request):
    servicio_id = request.GET.get("servicio")
    especialistas = Especialista.objects.filter(especialidades__id=servicio_id)
    return render(
        request, "especialistas_opciones.html", {"especialistas": especialistas}
    )


def get_horas_disponibles(request):
    fecha = request.GET.get("fecha")
    especialista_id = request.GET.get("especialista")
    horas = calculate_available_hours(fecha, especialista_id)
    return render(request, "horas_disponibles.html", {"horas": horas})
