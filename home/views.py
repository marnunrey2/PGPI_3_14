from django.shortcuts import render
from citas.models import Servicio, Especialista


def HomeView(request):
    return render(request, "home/home.html")


def perfil(request):
    #citas = Citas.objects.filter(usuario=self.user)
    return render(request, "home/perfil.html")

def servicios(request):
    servicios = Servicio.objects.all()
    context = {"servicios": servicios}
    return render(request, "home/servicios.html", context)


def especialistas(request):
    especialistas = Especialista.objects.all()
    context = {"especialistas": especialistas}
    return render(request, "home/especialistas.html", context)

