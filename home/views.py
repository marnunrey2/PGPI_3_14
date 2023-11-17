from django.shortcuts import render


def home(request):
    return render(request, "home/home.html")


def perfil(request):
    return render(request, "home/perfil.html")
