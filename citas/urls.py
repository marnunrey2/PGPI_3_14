from django.urls import path
from .views import (
    CitaView,
    ConsultaView,
    get_especialistas_por_servicio,
    get_horas_disponibles,
    cita_delete,
    get_servicios_por_especialista,
)


urlpatterns = [
    path(
        "especialistas_opciones/",
        get_especialistas_por_servicio,
        name="especialistas_opciones",
    ),
    path(
        "servicios_opciones/",
        get_servicios_por_especialista,
        name="servicios_opciones",
    ),
    path("horas_disponibles/", get_horas_disponibles, name="horas_disponibles"),
    path("cita/", CitaView.as_view(), name="cita"),
    path("citas/<int:cita_id>/delete/", cita_delete, name="cita_delete"),
    path("consulta/", ConsultaView.as_view(), name="consulta_citas"),
]
