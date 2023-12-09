from citas.models import PreCita
import stripe
from PGPI_3_14 import settings
from citas.models import Servicio


class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, precita):
        precita_dict = {
            "cita_id": precita.id,
            "servicio": precita.servicio.nombre,
            "especialista": precita.especialista.nombre,
            "fecha": precita.fecha.strftime("%Y-%m-%d"),
            "hora": precita.hora,
            "acumulado": float(get_precio_numerico_por_servicio(precita.servicio.id)),
            "cantidad": 1,
        }
        precita_id = str(precita.id)
        if precita_id not in self.carrito.keys():
            self.carrito[precita_id] = precita_dict
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, precita):
        id = str(precita.id)
        if id in self.carrito:
            PreCita.objects.filter(id=id).delete()
            del self.carrito[id]
            self.guardar_carrito()

    def limpiar(self):
        for precita_id in self.carrito.keys():
            PreCita.objects.filter(id=precita_id).delete()
        self.session["carrito"] = {}
        self.session.modified = True


def get_precio_numerico_por_servicio(id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        priceId = Servicio.objects.filter(id=id).get().precioId
        price = stripe.Price.retrieve(priceId)
        price_amount = price.get("unit_amount")
        price_str = str(price_amount)
        formatted_price = f"{price_str[:-2]}.{price_str[-2:]}"
    except Exception as e:
        formatted_price = "No disponible"
    return formatted_price
