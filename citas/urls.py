from django.urls import path
from .views import (
    CitaView,
    get_especialistas_por_servicio,
    get_horas_disponibles,
    cita_delete,
)


urlpatterns = [
    path(
        "especialistas_opciones/",
        get_especialistas_por_servicio,
        name="especialistas_opciones",
    ),
    path("horas_disponibles/", get_horas_disponibles, name="horas_disponibles"),
    path("cita/", CitaView.as_view(), name="cita"),
    path("citas/<int:cita_id>/delete/", cita_delete, name="cita_delete"),
]
