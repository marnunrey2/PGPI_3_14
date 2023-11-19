from django.urls import path
from .views import HomeView, servicios, especialistas
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", HomeView, name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="home/about.html"),
        name="about",
    ),
    path("perfil/", views.perfil, name="perfil"),
    path("servicios/", servicios, name="servicios"),
    path("especialistas/", especialistas, name="especialistas"),
    path("citas/<int:cita_id>/delete/", views.citaDelete),
    path("perfil/update_profile/", views.update_profile, name="update_profile"),
]
