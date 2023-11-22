from django.urls import path
from .views import HomeView, servicios, especialistas, perfil
from django.views.generic import TemplateView

urlpatterns = [
    path("", HomeView, name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="home/about.html"),
        name="about",
    ),
    path("servicios/", servicios, name="servicios"),
    path("especialistas/", especialistas, name="especialistas"),
    path("perfil/", perfil, name="perfil"),
]
