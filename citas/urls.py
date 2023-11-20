from django.urls import path
from .views import ReservaView, ServiciosView, CalendarioView


urlpatterns = [
    path("reserva/", ReservaView.as_view(), name="reserva"),
    path("servicios/", ServiciosView.as_view(), name="servicios"),
    path("calendario/", CalendarioView.as_view(), name="calendario"),
    # Add more URLs as needed
]
