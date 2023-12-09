from django.shortcuts import get_object_or_404, render, redirect
import stripe
from PGPI_3_14 import settings
from carrito.Carrito import Carrito
from citas.models import PreCita
from home.views import format_price
from rest_framework.views import APIView


class CarritoView(APIView):
    def get(self, request):
        return render(
            request,
            "carrito.html",
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
