from django.urls import path
from .views import (
    ServiciosView,
    CitaView,
    get_especialistas_por_servicio,
    get_horas_disponibles,
)


urlpatterns = [
    path("elige/", ServiciosView.as_view(), name="servicios"),
    path(
        "especialistas_opciones/",
        get_especialistas_por_servicio,
        name="especialistas_opciones",
    ),
    path("horas_disponibles/", get_horas_disponibles, name="horas_disponibles"),
]
