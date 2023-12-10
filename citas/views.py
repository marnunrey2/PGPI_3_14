import base64
import datetime
from django.utils import timezone
import os
from django.shortcuts import render, redirect, get_object_or_404
from carrito.Carrito import Carrito
from citas.forms import CitaServicioAddCarritoForm, CitaEspecialistaAddCarritoForm
import stripe
from django.shortcuts import render, redirect
from PGPI_3_14 import settings
from rest_framework.views import APIView
from citas.models import Especialista, Invitado, Cita, Servicio, PreCita
from .utils import calculate_available_hours
from django.http import HttpResponse, HttpResponseForbidden
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os
from home.views import format_price


class CitaServicioAddView(APIView):
    def post(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        form = CitaServicioAddCarritoForm(request.POST, servicio=servicio)
        if form.is_valid():
            especialista_id = form.cleaned_data["especialista"].id
            fecha = form.cleaned_data["fecha"].strftime("%Y-%m-%d")
            hora = form.cleaned_data["hora"]

            precita = PreCita.objects.create(
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
            )

            carrito = Carrito(request)
            carrito.agregar(precita)

            my_data = {"success_message": "Su cita ha sido añadida al carrito"}
            response = redirect("/carrito")
            response["Location"] += f'?key={my_data["success_message"]}'
            return response

        else:
            msg = "Error en el formulario"
            print(form.errors)
            return render(
                request, "cita_servicio_add_carrito.html", {"form": form, "msg": msg}
            )

    def get(self, request, servicio_id):
        servicio = get_object_or_404(Servicio, id=servicio_id)
        form = CitaServicioAddCarritoForm(
            servicio=servicio,
        )
        return render(
            request,
            "cita_servicio_add_carrito.html",
            {"form": form, "servicio": servicio},
        )


class CitaEspecialistaAddView(APIView):
    def post(self, request, especialista_id):
        especialista = get_object_or_404(Especialista, id=especialista_id)
        form = CitaEspecialistaAddCarritoForm(request.POST, especialista=especialista)
        if form.is_valid():
            servicio_id = form.cleaned_data["servicio"].id
            fecha = form.cleaned_data["fecha"].strftime("%Y-%m-%d")
            hora = form.cleaned_data["hora"]

            precita = PreCita.objects.create(
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
            )
            carrito = Carrito(request)
            carrito.agregar(precita)

            my_data = {"success_message": "Su cita ha sido añadida al carrito"}
            response = redirect("/carrito")
            response["Location"] += f'?key={my_data["success_message"]}'
            return response

        else:
            msg = "Error en el formulario"
            return render(
                request,
                "cita_especialista_add_carrito.html",
                {"form": form, "msg": msg},
            )

    def get(self, request, especialista_id):
        especialista = get_object_or_404(Especialista, id=especialista_id)
        form = CitaEspecialistaAddCarritoForm(especialista=especialista)
        return render(
            request,
            "cita_especialista_add_carrito.html",
            {"form": form, "especialista": especialista},
        )


class CitasView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            citas_pasadas = Cita.objects.filter(
                fecha__lt=timezone.now(), usuario=request.user
            )
            citas_futuras = Cita.objects.filter(
                fecha__gte=timezone.now(), usuario=request.user
            )
            return render(
                request,
                "citas.html",
                {
                    "citas_pasadas": citas_pasadas,
                    "citas_futuras": citas_futuras,
                    "success_message": request.GET.get("key"),
                },
            )
        else:
            return redirect("/")


def consulta_email(request, **kwargs):
    encoded = kwargs.get("encoded", 0)
    decode = base64.b64decode(str(encoded)).decode("utf-8")
    citaId = decode.replace("salt", "")
    cita = Cita.objects.get(pk=citaId)
    return render(request, "citas_invitado.html", {"cita": cita, "hash": encoded})


def get_especialistas_por_servicio(request):
    servicio_id = request.GET.get("servicio")
    especialistas = Especialista.objects.filter(especialidades__id=servicio_id)
    return render(
        request, "especialistas_opciones.html", {"especialistas": especialistas}
    )


def get_precio_por_servicio(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        servicio_id = request.GET.get("servicio")
        priceId = Servicio.objects.filter(id=servicio_id).get().precioId
        price = stripe.Price.retrieve(priceId)
        price_amount = price.get("unit_amount")
        formated_price = format_price(price_amount)
    except Exception as e:
        formated_price = "No disponible"
    return render(request, "precio.html", {"priceId": formated_price})


def get_precio_por_servicio(id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        priceId = Servicio.objects.filter(id=id).get().precioId
        price = stripe.Price.retrieve(priceId)
        price_amount = price.get("unit_amount")
        formated_price = format_price(price_amount)
    except Exception as e:
        formated_price = "No disponible"
    return formated_price


def get_precio_id_por_servicio(request):
    try:
        servicio_id = request.GET.get("servicio")
        priceId = Servicio.objects.filter(id=servicio_id).get().precioId
    except Exception as e:
        priceId = "No disponible"
    return render(request, "precio_id.html", {"priceId": priceId})


def get_estado_id_por_servicio(request):
    servicio_id = request.GET.get("servicio")
    if not servicio_id:  # Check if the 'servicio' ID is empty
        return HttpResponse("Disponible")  # Return a default value
    try:
        servicio = Servicio.objects.get(id=servicio_id)
        estado_agotado = servicio.agotado
        estado_texto = "Agotado" if estado_agotado else "Disponible"
    except Servicio.DoesNotExist:
        estado_texto = "Disponible"  # Set default value to "Disponible" if the service ID is not available
    return HttpResponse(estado_texto)


def get_precio_id_por_servicio_string(id):
    try:
        price_id = Servicio.objects.filter(id=id).get().precioId
    except Exception as e:
        redirect("../checkout/error")
        return None
    return price_id


def get_servicios_por_especialista(request):
    especialista_id = request.GET.get("especialista")
    servicios = Servicio.objects.filter(especialistas=especialista_id)
    options = '<option value="">-----</option>'
    for servicio in servicios:
        options += f'<option value="{servicio.id}">{servicio.nombre}</option>'
    return HttpResponse(options)


def get_horas_disponibles(request):
    fecha = request.GET.get("fecha")
    especialista_id = request.GET.get("especialista")
    horas = calculate_available_hours(fecha, especialista_id)
    return render(request, "horas_disponibles.html", {"horas": horas})


def cita_delete(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)
    if ((cita.fecha -datetime.date.today()).days<=1):
        my_data = {"success_message": "No se puede cancelar citas cuando queda menos de 1 día para ella"}
        response = redirect("/")
        response["Location"] += f'?key={my_data["success_message"]}'
        return response

    if request.user == cita.usuario:
        cita.delete()
        return redirect("/citas")
    elif request.user.is_staff:
        cita.delete()
        return redirect("/admin_view/citas")
    else:
        return HttpResponseForbidden()

def cita_delete_invitado(request, **kwargs):
    cita_encode = kwargs.get("encoded", 0)
    decode = base64.b64decode(str(cita_encode)).decode("utf-8")
    citaId = decode.replace("salt", "")
    cita = get_object_or_404(Cita, pk=citaId)
    if ((cita.fecha -datetime.date.today()).days<=1):
        my_data = {"success_message": "No se puede cancelar citas cuando queda menos de 1 día para ella"}
        response = redirect("/")
        response["Location"] += f'?key={my_data["success_message"]}'
        return response
    cita.delete()
    return redirect("/")
