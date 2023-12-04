import base64
import os
from django.shortcuts import render, redirect, get_object_or_404
from citas.forms import CitaServicioAddForm, CitaEspecialistaAddForm
import stripe
from django.shortcuts import render, redirect

import payments.views
from PGPI_3_14 import settings
from rest_framework.views import APIView
from citas.models import Especialista, Invitado, Cita, Servicio
from citas.models import Servicio, Especialista, Invitado, Cita
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime, timedelta
from .utils import calculate_available_hours
from datetime import datetime
from django.http import HttpResponseForbidden
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os

from payments import views
from django.views.generic.base import TemplateView


class CitaServicioAddView(APIView):
    def post(self, request):
        form = CitaServicioAddForm(request.POST)
        if form.is_valid():
            servicio_id = form.cleaned_data["servicio"].id
            especialista_id = form.cleaned_data["especialista"].id
            fecha = form.cleaned_data["fecha"].strftime("%Y-%m-%d")
            hora = form.cleaned_data["hora"]
            metodo_pago = form.cleaned_data["metodo_pago"]

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
                pagado=False,
                metodo_pago=metodo_pago
            )
            if usuario is not None:
                email = usuario.email
            mailMessage = Mail(
                from_email='aestheticarepgpi@gmail.com',
                to_emails=email,
                )
            idEncode = f'salt{cita.pk}'
            encoded = base64.b64encode(bytes(idEncode, encoding='utf-8')).decode('utf-8')
            urlVerificar =f"{request.build_absolute_uri()}/{encoded}"
            mailMessage.dynamic_template_data = {"urlVerificar":urlVerificar,
                                                 "fecha":fecha, "hora":hora, "servicio":Servicio.objects.get(pk=servicio_id).nombre, "especialista":Especialista.objects.get(pk=especialista_id).nombre
                                                 }
            mailMessage.template_id = "d-268e15e8ae4f4753b248b5b279a81c9d"
            load_dotenv()
            print(os.getenv("SENDGRID_API_KEY"))
            sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
            response = sg.send(mailMessage)
            if metodo_pago == "TA":
                priceId = get_precio_id_por_servicio_string(servicio_id)
                return render(request, "pay.html", {"priceId": priceId, "citaId": cita.id, "fecha": fecha, "hora": hora})
            else:
                return render(request, "home/home.html", {"cita": cita})

        else:
            msg = "Error en el formulario"
            return render(request, "cita_servicio_add.html", {"form": form, "msg": msg})

    def get(self, request):
        form = CitaServicioAddForm(user=request.user)
        return render(
            request,
            "cita_servicio_add.html",
            {"form": form},
        )


class CitaEspecialistaAddView(APIView):
    def post(self, request):
        form = CitaEspecialistaAddForm(request.POST)
        if form.is_valid():
            servicio_id = form.cleaned_data["servicio"].id
            especialista_id = form.cleaned_data["especialista"].id
            fecha = form.cleaned_data["fecha"].strftime("%Y-%m-%d")
            hora = form.cleaned_data["hora"]
            metodo_pago = form.cleaned_data["metodo_pago"]

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
                pagado=False,
                metodo_pago=metodo_pago
            )
            if usuario is not None:
                email = usuario.email
            mailMessage = Mail(
                from_email='aestheticarepgpi@gmail.com',
                to_emails=email,
                )
            idEncode = f'salt{cita.pk}'
            encoded = base64.b64encode(bytes(idEncode, encoding='utf-8')).decode('utf-8')
            urlVerificar =f"{request.build_absolute_uri()}/{encoded}"
            mailMessage.dynamic_template_data = {"urlVerificar":urlVerificar,
                                                 "fecha":fecha, "hora":hora, "servicio":Servicio.objects.get(pk=servicio_id).nombre, "especialista":Especialista.objects.get(pk=especialista_id).nombre
                                                 }
            mailMessage.template_id = "d-268e15e8ae4f4753b248b5b279a81c9d"
            load_dotenv()
            print(os.getenv("SENDGRID_API_KEY"))
            sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
            response = sg.send(mailMessage)
            if metodo_pago == "TA":
                priceId = get_precio_id_por_servicio_string(servicio_id)
                return render(request, "pay.html",
                              {"priceId": priceId, "citaId": cita.id, "fecha": fecha, "hora": hora})
            else:
                return render(request, "home/home.html", {"cita": cita})

        else:
            msg = "Error en el formulario"
            print(form.errors)
            return render(
                request, "cita_especialista_add.html", {"form": form, "msg": msg}
            )

    def get(self, request):
        form = CitaEspecialistaAddForm(user=request.user)
        return render(
            request,
            "cita_especialista_add.html",
            {"form": form},
        )


def consulta_email(request,  **kwargs):
    encoded = kwargs.get("encoded", 0)
    email = request.POST.get("email", None)
    decode =base64.b64decode(str(encoded)).decode('utf-8')
    citaId =decode.replace("salt", "")
    cita = Cita.objects.get(pk=citaId)
    return render(request, "citas_invitado.html", {"cita": cita, "hash":encoded})

def get_especialistas_por_servicio(request):
    servicio_id = request.GET.get("servicio")
    especialistas = Especialista.objects.filter(especialidades__id=servicio_id)
    return render(
        request, "especialistas_opciones.html", {"especialistas": especialistas}
    )

def format_price(price_amount):
    try:
        # Convert the price amount to a string
        price_str = str(price_amount)

        # Separate the first two digits from the last two digits with a comma
        formatted_price = f"{price_str[:-2]},{price_str[-2:]}"

        # Append Euro symbol at the end
        formatted_price += " €"
    except Exception as e:
        formatted_price = "No disponible"

    return formatted_price


def get_precio_por_servicio(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        servicio_id = request.GET.get("servicio")
        priceId = Servicio.objects.filter(id=servicio_id).get().precioId
        price = stripe.Price.retrieve(priceId)
        price_amount = price.get('unit_amount')
        formated_price = format_price(price_amount)
    except Exception as e:
        formated_price = "No disponible"
    return render(
        request, "precio.html", {"priceId": formated_price}
    )

def get_precio_id_por_servicio(request):
    try:
        servicio_id = request.GET.get("servicio")
        priceId = Servicio.objects.filter(id=servicio_id).get().precioId
    except Exception as e:
        priceId = "No disponible"
    return render(
        request, "precio_id.html", {"priceId": priceId}
    )

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
    return render(request, "servicios_opciones.html", {"servicios": servicios})


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
