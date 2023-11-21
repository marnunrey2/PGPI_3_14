from django.urls import path
from .views import ServiciosView, CitaView, get_especialistas_por_servicio


urlpatterns = [
    path("elige/", ServiciosView.as_view(), name="servicios"),
    path("cita/", CitaView.as_view(), name="cita"),
    path(
        "especialistas_opciones/",
        get_especialistas_por_servicio,
        name="especialistas_opciones",
    ),
]
