from django.conf import settings
from django.urls import path
from .views import (
    get_especialistas_por_servicio,
    get_estado_id_por_especialista,
    get_estado_id_por_servicio,
    get_horas_disponibles,
    get_precio_por_servicio,
    get_precio_id_por_servicio,
    cita_delete,
    cita_delete_invitado,
    consulta_email,
    get_servicios_por_especialista,
    CitasView,
    CitaServicioAddView,
    CitaEspecialistaAddView,
)
from payments import views as views


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
    path("precio_servicio/", get_precio_por_servicio, name="precio"),
    path("precio_id_servicio/", get_precio_id_por_servicio, name="precioid"),
    path("estado_id_servicio/", get_estado_id_por_servicio, name="estado_servicio"),
    path(
        "estado_id_especialista/",
        get_estado_id_por_especialista,
        name="estado_especialista",
    ),
    path("citas/servicios/utils/config/", views.stripe_config),
    path(
        "citas/servicios/utils/create-custom-checkout-session/<str:param>/<str:ident>",
        views.create_custom_checkout_session,
    ),
    path("citas/especialistas/utils/config/", views.stripe_config),
    path(
        "citas/especialistas/utils/create-custom-checkout-session/<str:param>/<str:ident>",
        views.create_custom_checkout_session,
    ),
    path("citas/success/", views.SuccessView.as_view(), name="success"),
    path("citas/cancelled/", views.CancelledView.as_view(), name="cancelled"),
    path("citas/webhook/", views.stripe_webhook),
    path("citas/<str:cita_id>/delete/", cita_delete, name="cita_delete"),
    path("citas/<str:encoded>/deleteinvitado", cita_delete_invitado),
    path("citas/", CitasView.as_view(), name="citas"),
    path(
        "citas/servicios/add/<int:servicio_id>",
        CitaServicioAddView.as_view(),
        name="cita_servicio_add",
    ),
    path(
        "citas/especialistas/add/<int:especialista_id>",
        CitaEspecialistaAddView.as_view(),
        name="cita_especialista_add",
    ),
    path("citas/", CitasView.as_view(), name="citas"),
    path("citas/<str:encoded>", consulta_email, name="consulta_email"),
]


from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
