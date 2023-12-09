from citas.models import Cita
from .views import get_precio_numerico_por_servicio


class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session["carrito"]
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, cita):
        id = str(cita.id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "cita_id": cita.id,
                "servicio": cita.servicio,
                "especialista": cita.especialista,
                "fecha": cita.fecha,
                "hora": cita.hora,
                "acumulado": float(get_precio_numerico_por_servicio(cita.servicio.id)),
                "cantidad": 1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += float(
                get_precio_numerico_por_servicio(cita.servicio.id)
            )
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, cita):
        id = str(cita.id)
        if id in self.carrito:
            Cita.objects.filter(id=id).delete()
            del self.carrito[id]
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True
