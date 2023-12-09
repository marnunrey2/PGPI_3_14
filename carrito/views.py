from django.shortcuts import render
import stripe
from PGPI_3_14 import settings
from carrito import Carrito
from citas.models import Servicio
from home.views import format_price
from rest_framework.views import APIView


class CarritoView(APIView):
    def get(self, request):
        return render(
            request,
            "carrito.html",
        )


def get_precio_numerico_por_servicio(id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        priceId = Servicio.objects.filter(id=id).get().precioId
        price = stripe.Price.retrieve(priceId)
        price_amount = price.get("unit_amount")
    except Exception as e:
        price_amount = "No disponible"
    return price_amount
