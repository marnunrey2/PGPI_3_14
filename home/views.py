import base64

import stripe
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash

from PGPI_3_14 import settings
from citas.models import Cita, Servicio, Especialista
from django.contrib import messages
from authentication.forms import (
    UpdateProfileForm,
)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render

from citas.views import format_price


def perfil(request):
    return render(request, "home/perfil.html")


def servicios(request):
    servicios = Servicio.objects.all()
    for servicio in servicios:
        servicio.precio = get_precio_por_servicio(servicio.id)
    context = {"servicios": servicios}
    return render(request, "home/home.html", context)


def especialistas(request):
    especialistas = Especialista.objects.all()
    context = {"especialistas": especialistas}
    return render(request, "home/especialistas.html", context)


def update_profile(request):
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors)

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


def get_precio_por_servicio(id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        priceId = Servicio.objects.filter(id=id).get().precioId
        price = stripe.Price.retrieve(priceId)
        price_amount = price.get("unit_amount")
        formated_price = format_price(price_amount)
    except Exception as e:
        formated_price = "No disponible"
    return formated_price
