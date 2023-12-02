from django.urls import path
from .views import (
    ReclamacionView,
    ReclamacionAddView,
)

urlpatterns = [
    path(
        "reclamaciones/",
        ReclamacionView.as_view(),
        name="reclamaciones",
    ),
    path(
        "reclamaciones/<int:cita_id>/add",
        ReclamacionAddView.as_view(),
        name="reclamacion_add",
    ),
]
