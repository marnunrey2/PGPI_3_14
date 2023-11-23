from django.urls import path
from .views import (
    CitaView,
    get_especialistas_por_servicio,
    get_horas_disponibles,
    consultar_citas_invitado,
)


urlpatterns = [
    path(
        "especialistas_opciones/",
        get_especialistas_por_servicio,
        name="especialistas_opciones",
    ),
    path("horas_disponibles/", get_horas_disponibles, name="horas_disponibles"),
    path("cita/", CitaView.as_view(), name="cita"),
    path("consulta/", consultar_citas_invitado, name="consulta_citas"),
]
