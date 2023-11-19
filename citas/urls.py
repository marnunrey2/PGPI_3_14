from django.urls import path
from .views import ReservaView, CalendarioView


urlpatterns = [
    path("reserva/", ReservaView.as_view(), name="reserva"),
    path("calendario/", CalendarioView.as_view(), name="calendario"),
    # Add more URLs as needed
]
