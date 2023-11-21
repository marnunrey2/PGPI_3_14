from django.shortcuts import render, redirect
from .forms import SerEspForm, CitaUsuario, CitaInvitado
from rest_framework.views import APIView
from citas.models import Servicio, Especialista, Invitado, Cita
from django.http import JsonResponse


class ServiciosView(APIView):
    def post(self, request):
        form = SerEspForm(request.POST)
        if form.is_valid():
            servicio = form.cleaned_data["servicio"]
            especialista = form.cleaned_data["especialista"]
            if request.user.is_authenticated:
                form = CitaUsuario()
                context = {
                    "servicio": servicio,
                    "especialista": especialista,
                    "form": form,
                }
                return render(request, "crear_cita_usuario.html", context)
            else:
                form = CitaInvitado()
                context = {
                    "servicio": servicio,
                    "especialista": especialista,
                    "form": form,
                }
                return render(request, "crear_cita_invitado.html", context)
        else:
            msg = "Error en el formulario"
            return render(request, "home/home.html", {"form": form, "msg": msg})

    def get(self, request):
        form = SerEspForm()
        return render(
            request,
            "elige.html",
            {"form": form},
        )


def get_especialistas_por_servicio(request):
    servicio_id = request.GET.get("servicio")
    especialistas = Especialista.objects.filter(especialidades__id=servicio_id)
    return render(
        request, "especialistas_opciones.html", {"especialistas": especialistas}
    )


class CitaView(APIView):
    def post(self, request):
        """
        user_id: id
        nombre: nombre
        email: email
        telefono: telefono
        selected_date: fecha
        selected_time_slot: hora
        servicio: nombre
        especialista: nombre
        """
        fecha = request.data.get("selected_date")
        hora = request.data.get("selected_time_slot")
        servicio_nombre = request.data.get("servicio")
        servicio_id = Servicio.objects.get(nombre=servicio_nombre).id
        especialista_nombre = request.data.get("especialista")
        especialista_id = Especialista.objects.get(nombre=especialista_nombre).id
        user_id = request.data.get("user_id")
        if user_id == "None":
            nombre = request.data.get("nombre")
            email = request.data.get("email")
            telefono = request.data.get("telefono")
            invitado = Invitado.objects.create(
                nombre=nombre, email=email, telefono=telefono
            )
            cita = Cita.objects.create(
                invitado_id=invitado.id,
                fecha=fecha,
                hora=hora,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
            )
        else:
            cita = Cita.objects.create(
                usuario=user_id,
                fecha=fecha,
                hora=hora,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
            )

        return render(request, "home.html")

    def get(self, request):
        pass
