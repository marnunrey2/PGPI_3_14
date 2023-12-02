from django.conf import settings
from django.urls import path
from .views import (
    HomeView,
    servicios,
    especialistas,
    perfil,
    update_password,
    update_profile,
)
from django.views.generic import TemplateView

app_name = "home"

urlpatterns = [
    path("", HomeView, name="home"),
    path("servicios/", servicios, name="servicios"),
    path("especialistas/", especialistas, name="especialistas"),
    path(
        "about/",
        TemplateView.as_view(template_name="home/about.html"),
        name="about",
    ),
    path("perfil/", perfil, name="perfil"),
    path("perfil/update_profile", update_profile, name="update_profile"),
    path("perfil/update_password", update_password, name="update_password"),
]
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
