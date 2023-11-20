from django.shortcuts import render, redirect
from .forms import ServicioEspecialistaForm, ClientInfoForm
from rest_framework.views import APIView
from citas.models import Servicio, Especialista, Invitado, Cita
from django.http import JsonResponse


class ServiciosView(APIView):
    def post(self, request):
        form = ServicioEspecialistaForm(request.POST)
        if form.is_valid():
            servicio = form.cleaned_data.get("servicio")
            especialista = form.cleaned_data.get("especialista")
            context = {"servicio": servicio, "especialista": especialista}
            return render(
                request,
                "calendario.html",
                context,
            )
        else:
            msg = "Error en el formulario"
            return render(request, "home/home.html", {"form": form, "msg": msg})
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
            "elige_servicios.html",
            {"form": form, "servicios": servicios, "especialistas": especialistas},
        )


class CalendarioView(APIView):
    def post(self, request):
        form = request.data.get("form")
        return render(
            request,
            "reserva.html",
            {"form": form},
        )

    def get(self, request):
        form = request.data.get("form")
        return render(
            request,
            "calendario.html",
            {"form": form},
        )


class ReservaView(APIView):
    def post(self, request):
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            # If the form is valid, create an Invitado instance
            nombre = form["nombre"]
            email = form["email"]
            telefono = form["telefono"]

            invitado = Invitado.objects.create(
                nombre=nombre, email=email, telefono=telefono
            )

            form.save()

            return redirect("/")
        else:
            form = ClientInfoForm()
            msg = "Error de formulario"
            return render(
                request,
                "reserva.html",
                {"form": form, "msg": msg},
            )

    def get(self, request):
        form = ClientInfoForm(None)
        return render(
            request,
            "reserva.html",
            {"form": form},
        )


class CitaView(APIView):
    def post(self, request):
        """
        user_id: id
        selected_date: fecha
        selected_time_slot: hora
        servicio: nombre
        especialista: nombre
        """
        user_id = request.data.get("user_id")
        fecha = request.data.get("selected_date")
        hora = request.data.get("selected_time_slot")
        servicio_nombre = request.data.get("servicio")
        especialista_nombre = request.data.get("especialista")
        cita = Cita.objects.create(
            usuario_id=user_id,
            fecha=fecha,
            hora=hora,
            servicio_id=servicio_nombre,
            especialista_id=especialista_nombre,
        )
        return JsonResponse(
            {"status": "success", "message": "Cita created successfully"}
        )

    def get(self, request):
        return render(
            request,
            "calendario.html",
        )
