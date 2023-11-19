from django.shortcuts import render
from citas.models import Cita


def HomeView(request):
    return render(request, "home/home.html")


def perfil(request):
    citas = Cita.objects.filter(usuario=request.user)
    citas = citas.order_by("-fecha")
    return render(request, "home/perfil.html", {"citas":citas})
