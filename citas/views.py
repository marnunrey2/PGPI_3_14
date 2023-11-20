from django.shortcuts import render, redirect
from .forms import ServicioEspecialistaForm, ClientInfoForm
from rest_framework.views import APIView
from citas.models import Servicio, Especialista, Invitado


class ReservaView(APIView):
    def post(self, request):
        form = ClientInfoForm(request.POST)
        if form.is_valid():
            # If the form is valid, create an Invitado instance
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            telefono = form.cleaned_data["telefono"]

            invitado = Invitado.objects.create(
                nombre=nombre, email=email, telefono=telefono
            )

            return render(
                request,
                "servicios.html",
                {"invitado": invitado},
            )
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


class ServiciosView(APIView):
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
            "servicios.html",
            {"form": form, "servicios": servicios, "especialistas": especialistas},
        )


class CalendarioView(APIView):
    def post(self, request):
        form = request.data.get("form")
        return redirect("/")

    def get(self, request):
        form = request.data.get("form")
        return render(
            request,
            "calendario.html",
            {"form": form},
        )
