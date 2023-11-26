from django.urls import path, include
from .views import (
    AdminCitaView,
    AdminServicioView,
    servicio_delete,
    especialista_delete,
    AdminEspecialistaView,
    AdminUsuarioView,
    usuario_delete,
    AdminInvitadoView,
    invitado_delete,
    AdminServicioAddView,
    AdminEspecialistaAddView,
)

urlpatterns = [
    path("admin_view/citas", AdminCitaView.as_view(), name="admin_cita"),
    path("admin_view/servicios", AdminServicioView.as_view(), name="admin_servicio"),
    path(
        "servicios/<int:servicio_id>/delete/", servicio_delete, name="servicio_delete"
    ),
    path(
        "admin_view/especialistas",
        AdminEspecialistaView.as_view(),
        name="admin_especialista",
    ),
    path(
        "especialistas/<int:especialista_id>/delete/",
        especialista_delete,
        name="especialista_delete",
    ),
    path(
        "admin_view/usuarios",
        AdminUsuarioView.as_view(),
        name="admin_usuario",
    ),
    path(
        "usuarios/<int:usuario_id>/delete/",
        usuario_delete,
        name="usuario_delete",
    ),
    path(
        "admin_view/invitados",
        AdminInvitadoView.as_view(),
        name="admin_invitado",
    ),
    path(
        "invitados/<int:invitado_id>/delete/",
        invitado_delete,
        name="invitado_delete",
    ),
    path(
        "admin_view/servicios/add", AdminServicioAddView.as_view(), name="servicio_add"
    ),
    path(
        "admin_view/especialistas/add",
        AdminEspecialistaAddView.as_view(),
        name="especialista_add",
    ),
    path("", include(("home.urls", "home"), namespace="home")),
]
