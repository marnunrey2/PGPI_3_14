import base64
import os
from django.shortcuts import render, redirect, get_object_or_404
from citas.forms import CitaServicioAddForm, CitaEspecialistaAddForm
from rest_framework.views import APIView
from citas.models import Especialista, Invitado, Cita, Servicio
from .utils import calculate_available_hours
from datetime import datetime
from django.http import HttpResponseForbidden
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os



class CitaServicioAddView(APIView):
    def post(self, request):
        form = CitaServicioAddForm(request.POST)
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
            citaCreada = Cita.objects.create(
                usuario=usuario,
                invitado=invitado,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
            )
            if usuario is not None:
                email = usuario.email
            mailMessage = Mail(
                from_email='aestheticarepgpi@gmail.com',
                to_emails=email,
                )
            idEncode = f'salt{citaCreada.pk}'
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
            #print(response.status_code)
            #print(response.body)
            #print(response.headers)
            return redirect("/")

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

            usuario = request.user if request.user.is_authenticated else None
            invitado = None

            if usuario is None:
                nombre = form.cleaned_data["nombre"]
                email = form.cleaned_data["email"]
                telefono = form.cleaned_data["telefono"]

                invitado = Invitado.objects.create(
                    nombre=nombre, email=email, telefono=telefono
                )

            citaCreada = Cita.objects.create(
                usuario=usuario,
                invitado=invitado,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
            )
            if usuario is not None:
                email = usuario.email
            mailMessage = Mail(
                from_email='aestheticarepgpi@gmail.com',
                to_emails=email,
                )
            idEncode = f'salt{citaCreada.pk}'
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
            #print(response.status_code)
            #print(response.body)
            #print(response.headers)
            return redirect("/")

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
    return render(request, "citas_invitado.html", {"cita": cita})

def get_especialistas_por_servicio(request):
    servicio_id = request.GET.get("servicio")
    especialistas = Especialista.objects.filter(especialidades__id=servicio_id)
    return render(
        request, "especialistas_opciones.html", {"especialistas": especialistas}
    )


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
