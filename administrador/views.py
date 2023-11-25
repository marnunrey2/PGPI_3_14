from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from citas.models import Cita, Servicio, Especialista, Invitado
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User


class AdminCitaView(APIView):
    def get(self, request):
        if request.user.is_staff:
            citas = Cita.objects.all()
            context = {"citas": citas}
            return render(request, "admin_cita.html", context)
        else:
            return redirect("home:home")


class AdminServicioView(APIView):
    def get(self, request):
        if request.user.is_staff:
            servicios = Servicio.objects.all()
            context = {"servicios": servicios}
            return render(request, "admin_servicio.html", context)
        else:
            return redirect("home:home")


def servicio_delete(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)

    if request.user.is_staff:
        servicio.delete()
        return redirect("/admin_view/servicios")
    else:
        return HttpResponseForbidden()


class AdminEspecialistaView(APIView):
    def get(self, request):
        if request.user.is_staff:
            especialistas = Especialista.objects.all()
            context = {"especialistas": especialistas}
            return render(request, "admin_especialista.html", context)
        else:
            return redirect("home:home")


def especialista_delete(request, especialista_id):
    especialista = get_object_or_404(Especialista, pk=especialista_id)

    if request.user.is_staff:
        especialista.delete()
        return redirect("/admin_view/especialistas")
    else:
        return HttpResponseForbidden()


class AdminUsuarioView(APIView):
    def get(self, request):
        if request.user.is_staff:
            usuarios = User.objects.all()
            context = {"usuarios": usuarios}
            return render(request, "admin_usuario.html", context)
        else:
            return redirect("home:home")


def usuario_delete(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)

    if request.user.is_staff:
        usuario.delete()
        return redirect("/admin_view/usuarios")
    else:
        return HttpResponseForbidden()


class AdminInvitadoView(APIView):
    def get(self, request):
        if request.user.is_staff:
            invitados = Invitado.objects.all()
            context = {"invitados": invitados}
            return render(request, "admin_invitado.html", context)
        else:
            return redirect("home:home")


def invitado_delete(request, invitado_id):
    invitado = get_object_or_404(Invitado, pk=invitado_id)

    if request.user.is_staff:
        invitado.delete()
        return redirect("/admin_view/invitados")
    else:
        return HttpResponseForbidden()
