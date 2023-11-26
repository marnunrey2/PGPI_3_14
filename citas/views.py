from django.shortcuts import render, redirect, get_object_or_404
from .forms import CitaForm
from rest_framework.views import APIView
from citas.models import Especialista, Invitado, Cita
from .utils import calculate_available_hours
from datetime import datetime
from django.http import HttpResponseForbidden


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

            Cita.objects.create(
                usuario=usuario,
                invitado=invitado,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
            )
            return render(request, "home/home.html")

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


class ConsultaView(APIView):
    def post(self, request):
        nombre = request.POST.get("nombre", None)
        email = request.POST.get("email", None)

        if email:
            invitado = Invitado.objects.filter(email=email)
        else:
            msg = "Rellene el formulario"
            return render(request, "consulta_citas.html", {"msg": msg})

        if invitado:
            return render(request, "citas_invitado.html", {"invitado": invitado})
        else:
            # Manejar el caso de invitado no existente
            msg = "No hay ninguna cita con ese nombre o email"
            return render(request, "consulta_citas.html", {"msg": msg})

    def get(self, request):
        return render(request, "consulta_citas.html")


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


def cita_delete(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)

    if request.user == cita.usuario:
        cita.delete()
        return redirect("/")
    elif request.user.is_staff:
        cita.delete()
        return redirect("/admin_view/citas")
    else:
        return HttpResponseForbidden()
