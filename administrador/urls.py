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
    AdminUsuarioAddView,
    AdminCitaServicioAdd,
    AdminCitaEspecialistaAdd,
    AdminInvitadoAddView,
    AdminReclamacionView,
    AdminReclamacionAddView,
    reclamacion_delete,
)


urlpatterns = [
    path("admin_view/citas", AdminCitaView.as_view(), name="admin_cita"),
    path(
        "admin_view/citas/servicios/add",
        AdminCitaServicioAdd.as_view(),
        name="admin_cita_servicio_add",
    ),
    path(
        "admin_view/citas/especialistas/add",
        AdminCitaEspecialistaAdd.as_view(),
        name="admin_cita_especialista_add",
    ),
    path("admin_view/servicios", AdminServicioView.as_view(), name="admin_servicio"),
    path(
        "admin_view/servicios/add", AdminServicioAddView.as_view(), name="servicio_add"
    ),
    path(
        "servicios/<int:servicio_id>/delete/", servicio_delete, name="servicio_delete"
    ),
    path(
        "admin_view/especialistas",
        AdminEspecialistaView.as_view(),
        name="admin_especialista",
    ),
    path(
        "admin_view/especialistas/add",
        AdminEspecialistaAddView.as_view(),
        name="especialista_add",
    ),
    path(
        "especialistas/<int:especialista_id>/delete/",
        especialista_delete,
        name="especialista_delete",
    ),
    path(
        "admin_view/reclamaciones",
        AdminReclamacionView.as_view(),
        name="admin_reclamacion",
    ),
    path(
        "admin_view/reclamaciones/<int:cita_id>/add",
        AdminReclamacionAddView.as_view(),
        name="reclamacion_add",
    ),
    path(
        "reclamaciones/<int:reclamacion_id>/delete/",
        reclamacion_delete,
        name="reclamacion_delete",
    ),
    path(
        "admin_view/usuarios",
        AdminUsuarioView.as_view(),
        name="admin_usuario",
    ),
    path(
        "admin_view/usuarios/add",
        AdminUsuarioAddView.as_view(),
        name="usuario_add",
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
        "admin_view/invitados/add", AdminInvitadoAddView.as_view(), name="invitado_add"
    ),
    path(
        "invitados/<int:invitado_id>/delete/",
        invitado_delete,
        name="invitado_delete",
    ),
    path("", include(("home.urls", "home"), namespace="home")),
]
