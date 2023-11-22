from django.urls import path
from .views import HomeView, servicios, especialistas, perfil, citaDelete, update_profile
from django.views.generic import TemplateView

urlpatterns = [
    path("", HomeView, name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="home/about.html"),
        name="about",
    ),
    path("perfil/", perfil, name="perfil"),
    path("servicios/", servicios, name="servicios"),
    path("especialistas/", especialistas, name="especialistas"),
    path("citas/<int:cita_id>/delete/", citaDelete),
    path("perfil/update_profile/", update_profile, name="update_profile"),
]
