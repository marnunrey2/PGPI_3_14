from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from citas.models import Cita, Servicio, Especialista, Invitado
from reclamaciones.models import Reclamacion
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .forms import (
    ServicioAddForm,
    EspecialistaAddForm,
    UsuarioAddForm,
    InvitadoAddForm,
    CitaServicioAddForm,
    CitaEspecialistaAddForm,
    ReclamacionAddForm,
)


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


class AdminReclamacionView(APIView):
    def get(self, request):
        if request.user.is_staff:
            reclamaciones = Reclamacion.objects.all()
            context = {"reclamaciones": reclamaciones}
            return render(request, "admin_reclamacion.html", context)
        else:
            return redirect("home:home")


def reclamacion_delete(request, reclamacion_id):
    reclamacion = get_object_or_404(Reclamacion, pk=reclamacion_id)

    if request.user.is_staff:
        reclamacion.delete()
        return redirect("/admin_view/reclamaciones")
    elif reclamacion.cita.usuario == request.user:
        reclamacion.delete()
        return redirect("/reclamaciones")
    else:
        return HttpResponseForbidden()


def cerrar_reclamacion(request, reclamacion_id):
    reclamacion = get_object_or_404(Reclamacion, id=reclamacion_id)

    if request.method == "POST":
        if reclamacion.estado == "Abierto":
            reclamacion.estado = "Cerrado"
        elif reclamacion.estado == "Cerrado":
            reclamacion.estado = "Abierto"
        reclamacion.save()

    return redirect("/admin_view/reclamaciones")


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


class AdminCitaServicioAdd(APIView):
    def post(self, request):
        form = CitaServicioAddForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            usuario = form.cleaned_data["usuario"]
            invitado = form.cleaned_data["invitado"]
            servicio_id = form.cleaned_data["servicio"].id
            especialista_id = form.cleaned_data["especialista"].id
            fecha = form.cleaned_data["fecha"].strftime("%Y-%m-%d")
            hora = form.cleaned_data["hora"]

            Cita.objects.create(
                usuario=usuario,
                invitado=invitado,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
                pagado=False,
            )
            return redirect("/admin_view/citas")
        else:
            msg = "Error en el formulario"
            return render(request, "admin_cita.html", {"form": form, "msg": msg})

    def get(self, request):
        if request.user.is_staff:
            form = CitaServicioAddForm()
            return render(request, "admin_cita_servicio_add.html", {"form": form})
        else:
            return redirect("home:home")


class AdminCitaEspecialistaAdd(APIView):
    def post(self, request):
        form = CitaServicioAddForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            usuario = form.cleaned_data["usuario"]
            invitado = form.cleaned_data["invitado"]
            servicio_id = form.cleaned_data["servicio"].id
            especialista_id = form.cleaned_data["especialista"].id
            fecha = form.cleaned_data["fecha"].strftime("%Y-%m-%d")
            hora = form.cleaned_data["hora"]

            Cita.objects.create(
                usuario=usuario,
                invitado=invitado,
                servicio_id=servicio_id,
                especialista_id=especialista_id,
                fecha=fecha,
                hora=hora,
                pagado=False,
            )
            return redirect("/admin_view/citas")
        else:
            msg = "Error en el formulario"
            return render(request, "admin_cita.html", {"form": form, "msg": msg})

    def get(self, request):
        if request.user.is_staff:
            form = CitaEspecialistaAddForm()
            return render(request, "admin_cita_especialista_add.html", {"form": form})
        else:
            return redirect("home:home")


class AdminServicioAddView(APIView):
    def post(self, request):
        form = ServicioAddForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_staff:
            nombre = form.cleaned_data["nombre"]
            descripcion = form.cleaned_data["descripcion"]
            if "imagen" in request.FILES:
                imagen = request.FILES["imagen"]
            else:
                imagen = None
            precio = form.cleaned_data["precioId"]
            Servicio.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                imagen=imagen,
                precioId=precio,
            )
            return redirect("/admin_view/servicios")
        else:
            msg = "Error en el formulario"
            return render(request, "admin_servicio.html", {"form": form, "msg": msg})

    def get(self, request):
        if request.user.is_staff:
            form = ServicioAddForm()
            return render(request, "admin_servicio_add.html", {"form": form})
        else:
            return redirect("home:home")


def editar_estado_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("nuevo_estado")
        servicio.agotado = nuevo_estado == "True"
        servicio.save()

    return redirect("/admin_view/servicios")


def editar_estado_especialista(request, especialista_id):
    especialista = get_object_or_404(Especialista, id=especialista_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("nuevo_estado")
        especialista.agotado = nuevo_estado == "True"
        especialista.save()

    return redirect("/admin_view/especialistas")


class AdminEspecialistaAddView(APIView):
    def post(self, request):
        form = EspecialistaAddForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            nombre = form.cleaned_data["nombre"]

            if "imagen" in request.FILES:
                imagen = request.FILES["imagen"]
            else:
                imagen = None
            especialidades = form.cleaned_data["especialidades"]
            especialista = Especialista.objects.create(
                nombre=nombre,
                imagen=imagen,
            )

            for servicio in especialidades:
                especialista.especialidades.add(servicio)

            return redirect("/admin_view/especialistas")
        else:
            msg = "Error en el formulario"
            return render(
                request, "admin_especialista.html", {"form": form, "msg": msg}
            )

    def get(self, request):
        if request.user.is_staff:
            form = EspecialistaAddForm()
            return render(request, "admin_especialista_add.html", {"form": form})
        else:
            return redirect("home:home")


class AdminReclamacionAddView(APIView):
    def post(self, request, cita_id):
        form = ReclamacionAddForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            cita = get_object_or_404(Cita, pk=cita_id)
            mensaje = form.cleaned_data["mensaje"]
            Reclamacion.objects.create(
                cita=cita,
                mensaje=mensaje,
                fecha=date.today(),
            )
            return redirect("/admin_view/reclamaciones")
        else:
            msg = "Error en el formulario"
            return render(
                request, "admin_reclamacion_add.html", {"form": form, "msg": msg}
            )

    def get(self, request, cita_id):
        if request.user.is_staff:
            cita = get_object_or_404(Cita, pk=cita_id)
            form = ReclamacionAddForm()
            return render(
                request, "admin_reclamacion_add.html", {"form": form, "cita": cita}
            )
        else:
            return redirect("home:home")


class AdminUsuarioAddView(APIView):
    def post(self, request):
        form = UsuarioAddForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            is_staff = True

            User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_staff=is_staff,
            )

            return redirect("/admin_view/usuarios")
        else:
            msg = "Error en el formulario"
            return render(request, "admin_usuario.html", {"form": form, "msg": msg})

    def get(self, request):
        if request.user.is_staff:
            form = UsuarioAddForm()
            return render(request, "admin_usuario_add.html", {"form": form})
        else:
            return redirect("home:home")


class AdminInvitadoAddView(APIView):
    def post(self, request):
        form = InvitadoAddForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]

            Invitado.objects.create(
                nombre=nombre,
                email=email,
            )

            return redirect("/admin_view/invitados")
        else:
            msg = "Error en el formulario"
            return render(request, "admin_invitado.html", {"form": form, "msg": msg})

    def get(self, request):
        if request.user.is_staff:
            form = InvitadoAddForm()
            return render(request, "admin_invitado_add.html", {"form": form})
        else:
            return redirect("home:home")
