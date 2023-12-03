from django.conf import settings
from django.urls import path
from .views import (
    get_especialistas_por_servicio,
    get_horas_disponibles,
    cita_delete,
    get_servicios_por_especialista,
    consulta_email,
    CitaEspecialistaAddView,
    CitaServicioAddView,
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
    path("citas/<int:cita_id>/delete/", cita_delete, name="cita_delete"),
    path(
        "citas/servicios/add",
        CitaServicioAddView.as_view(),
        name="cita_servicio_add",
    ),
    path(
        "citas/especialistas/add",
        CitaEspecialistaAddView.as_view(),
        name="cita_especialista_add",
    ),
    path("citas/servicios/add/<str:encoded>", consulta_email, name="consulta_citas")
]

from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
