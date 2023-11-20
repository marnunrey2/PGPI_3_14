from django.urls import path
from .views import ReservaView, ServiciosView, CalendarioView


urlpatterns = [
    path("elige_servicios/", ServiciosView.as_view(), name="servicios"),
    path("calendario/", CalendarioView.as_view(), name="calendario"),
    path("reserva/", ReservaView.as_view(), name="reserva"),
    # Add more URLs as needed
]
