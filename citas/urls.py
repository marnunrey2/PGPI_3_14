from django.urls import path
from .views import ReservaView


urlpatterns = [
    path("reserva/", ReservaView.as_view(), name="reserva"),
    # Add more URLs as needed
]
