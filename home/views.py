from django.shortcuts import render


def home(request):
    return render(request, "home/home.html")


def perfil(request):
    #citas = Citas.objects.filter(usuario=self.user)
    return render(request, "home/perfil.html")
