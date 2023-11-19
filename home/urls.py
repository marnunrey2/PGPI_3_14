from django.urls import path
from .views import HomeView
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", HomeView, name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="home/about.html"),
        name="about",
    ),
    path("perfil/", views.perfil, name="perfil")
]
