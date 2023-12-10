from django.urls import path
from .views import (
    ReclamacionView,
    ReclamacionAddView,
    ReclamacionInvitadoAddView,
)

urlpatterns = [
    path(
        "reclamaciones/",
        ReclamacionView.as_view(),
        name="reclamaciones",
    ),
    path(
        "reclamaciones/<str:cita_id>/add",
        ReclamacionAddView.as_view(),
        name="reclamacion_add",
    ),
    path(
        "reclamaciones/<str:cita_encode>/addhash",
        ReclamacionInvitadoAddView.as_view(),
        name="reclamacion_add",
    ),
]
