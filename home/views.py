from django.shortcuts import render
from citas.models import Cita
from citas.models import Servicio, Especialista


def HomeView(request):
    return render(request, "home/home.html")


def perfil(request):
    citas = Cita.objects.filter(usuario=request.user)
    citas = citas.order_by("-fecha")
    return render(request, "home/perfil.html", {"citas":citas})

def servicios(request):
    servicios = Servicio.objects.all()
    context = {"servicios": servicios}
    return render(request, "home/servicios.html", context)


def especialistas(request):
    especialistas = Especialista.objects.all()
    context = {"especialistas": especialistas}
    return render(request, "home/especialistas.html", context)
