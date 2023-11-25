from django.urls import path, include
from .views import AdminCitaView

urlpatterns = [
    path("admin_view/citas", AdminCitaView.as_view(), name="admin_cita"),
    path("", include(("home.urls", "home"), namespace="home")),
]
