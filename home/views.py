from django.shortcuts import render
from citas.models import Cita
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from citas.models import Servicio, Especialista
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib import messages
from django.shortcuts import redirect, render
from authentication.forms import (
    LoginForm,
    RegisterForm,
    UpdateProfileForm,
)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render


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
    Cita.objects.filter(id=cita_id).delete()
    success_message = "¡Cuenta eliminada exitosamente!"

    # Assuming your home page URL is named 'home'
    return render(request, "home/home.html", {"success_message": success_message})


def update_profile(request):
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

        else:
            messages.error(request, "Error al actualizar perfil.")

    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, "home/perfil.html", {"form": form})


def update_password(request):
    if request.method == "POST":
        # Set the password manually if it's provided in the form
        new_password = request.POST.get("new_password1", None)
        confirm_new_password = request.POST.get("new_password2", None)
        if new_password:
            if new_password == confirm_new_password:
                request.user.set_password(new_password)
                request.user.save()
                # Update session to avoid log out after password change
                update_session_auth_hash(request, request.user)
                messages.success(request, "Perfil actualizado correctamente.")
            else:
                messages.error(request, "Las contraseñas no coinciden.")

    return render(request, "home/perfil.html")
