from django.urls import path
from .views import HomeView
from django.views.generic import TemplateView

urlpatterns = [
    path("", HomeView, name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
]
