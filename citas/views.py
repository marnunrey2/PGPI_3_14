from django.shortcuts import render, redirect
from .forms import SerEspForm, CitaUsuario, CitaInvitado
from rest_framework.views import APIView
from citas.models import Servicio, Especialista, Invitado, Cita
from django.http import JsonResponse
from datetime import datetime, timedelta


class ServiciosView(APIView):
    def post(self, request):
        form = SerEspForm(request.POST)
        if form.is_valid():
            servicio = form.cleaned_data["servicio"]
            especialista = form.cleaned_data["especialista"]
            fecha = form.cleaned_data["fecha"]
            hora = form.cleaned_data["hora"]
            user_id = request.user.id
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
            return render(request, "home/home.html")

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


def get_horas_disponibles(request):
    fecha = request.GET.get("fecha")
    especialista_id = request.GET.get("especialista_id")
    horas = calculate_available_hours(fecha, especialista_id)
    return render(request, "horas_disponibles.html", {"horas": horas})


def calculate_available_hours(fecha, especialista_id):
    appointment_duration = timedelta(hours=1)
    available_hours = []

    # Convert the given fecha string to a datetime object
    fecha_datetime = datetime.strptime(fecha, "%Y-%m-%d")

    # Get the working hours for the especialista
    especialista = Especialista.objects.get(pk=especialista_id)
    working_start_time = datetime(
        fecha_datetime.year, fecha_datetime.month, fecha_datetime.day, 9, 0
    )
    working_end_time = datetime(
        fecha_datetime.year, fecha_datetime.month, fecha_datetime.day, 17, 0
    )

    # Get all citas for the given especialista on the specified fecha
    citas_for_especialista = Cita.objects.filter(
        especialista_id=especialista_id, fecha=fecha
    )

    # Create a set of booked time slots based on existing citas
    booked_time_slots = {cita.hora.strftime("%H:%M") for cita in citas_for_especialista}

    # Loop through the working hours and find available time slots
    current_hour = working_start_time
    while current_hour < working_end_time:
        current_time_str = current_hour.strftime("%H:%M")

        # Check if the current time slot is not booked
        if current_time_str not in booked_time_slots:
            available_hours.append(current_time_str)

        # Increment the current hour by the appointment duration
        current_hour += appointment_duration

    return available_hours


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
