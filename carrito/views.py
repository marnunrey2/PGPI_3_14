from django.shortcuts import get_object_or_404, render, redirect
import stripe
from PGPI_3_14 import settings
from carrito.Carrito import Carrito
from carrito.forms import TramitarReservaForm
from citas.models import Cita, Especialista, Invitado, PreCita, Servicio
from home.views import format_price
from rest_framework.views import APIView


class CarritoView(APIView):
    def post(self, request):
        form = TramitarReservaForm(request.POST, user=request.user)
        if form.is_valid():
            carrito = Carrito(request).carrito
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
            for precita_id, precita_data in carrito.items():
                precita = PreCita.objects.get(id=precita_id)
                servicio = get_object_or_404(Servicio, nombre=precita.servicio)
                especialista = get_object_or_404(
                    Especialista, nombre=precita.especialista
                )
                cita = Cita.objects.create(
                    usuario=usuario,
                    invitado=invitado,
                    servicio=servicio,
                    especialista=especialista,
                    fecha=precita.fecha,
                    hora=precita.hora,
                    pagado=False,
                    metodo_pago=metodo_pago,
                )
            carrito = Carrito(request)
            carrito.limpiar()
            if request.user.is_authenticated:
                my_data = {"success_message": "Su compra ha sido completada"}
                response = redirect("/citas")
                response["Location"] += f'?key={my_data["success_message"]}'
                return response
            else:
                my_data = {
                    "success_message": "Su compra ha sido completada, se le ha enviado un correo con los detalles de su reserva"
                }
                response = redirect("/")
                response["Location"] += f'?key={my_data["success_message"]}'
                return response
        else:
            msg = "Error en el formulario"
            print(form.errors)
            return render(
                request,
                "carrito.html",
                {"form": form, "msg": msg},
            )

    def get(self, request):
        form = TramitarReservaForm(user=request.user)
        return render(
            request,
            "carrito.html",
            {"form": form, "success_message": request.GET.get("key")},
        )


def eliminar_cita(request, cita_id):
    carrito = Carrito(request)
    precita = get_object_or_404(PreCita, pk=cita_id)
    carrito.eliminar(precita)
    my_data = {"success_message": "Su cita ha sido eliminada del carrito"}
    response = redirect("/carrito")
    response["Location"] += f'?key={my_data["success_message"]}'
    return response


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    my_data = {"success_message": "Su carrito ha sido limpiado"}
    response = redirect("/carrito")
    response["Location"] += f'?key={my_data["success_message"]}'
    return response
