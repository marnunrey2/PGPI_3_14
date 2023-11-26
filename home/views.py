from django.shortcuts import render
from citas.models import Cita
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from citas.models import Servicio, Especialista
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
import datetime


def HomeView(request):
    return render(request, "home/home.html")


def perfil(request):
    return render(request, "home/perfil.html")


def servicios(request):
    servicios = Servicio.objects.all()
    context = {"servicios": servicios}
    return render(request, "home/servicios.html", context)


def especialistas(request):
    especialistas = Especialista.objects.all()
    context = {"especialistas": especialistas}
    return render(request, "home/especialistas.html", context)


def citaDelete(request, cita_id):
    citaToDelete = Cita.objects.get(id=cita_id)
    if citaToDelete.fecha <= datetime.datetime.now().date() + datetime.timedelta(
        days=1
    ):
        return render(
            request,
            "home/home.html",
            {"message": "No puedes cancelar citas que se vayan a dar en 1 día"},
        )
    Cita.objects.filter(id=cita_id).delete()
    return redirect("/")


def update_profile(request):
    if request.method == "POST":
        new_username = request.POST.get("new_username")
        new_email = request.POST.get("new_email")
        new_password = request.POST.get("new_password")

        if not new_username:
            messages.error(request, "New username cannot be empty.")
            return redirect("perfil")

        # Update the username and email
        request.user.username = new_username
        request.user.email = new_email
        request.user.save()

        if new_password:
            # Update the password
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in
            messages.success(request, "Password updated successfully.")

        messages.success(request, "Profile updated successfully.")
        return redirect("perfil")

    return render(request, "home/perfil.html")
