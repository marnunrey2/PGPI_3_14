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
from django.db.models import Q
from fuzzywuzzy import fuzz


def perfil(request):
    return render(request, "home/perfil.html")


def servicios(request):
    query = request.GET.get("q")
    servicios = Servicio.objects.all()

    if query:
        # No exact matches found for services, perform fuzzy matching on service names
        servicios = Servicio.objects.filter(nombre__icontains=query)
        service_matches = [
            (servicio, fuzz.partial_ratio(query, servicio.nombre))
            for servicio in servicios
        ]
        service_matches.sort(key=lambda x: x[1], reverse=True)  # Sort by similarity

        # Filter results to those with a similarity ratio above a certain threshold (adjust as needed)
        threshold = 50
        service_matches = [
            match[0] for match in service_matches if match[1] > threshold
        ]

        servicios = service_matches

        # If no service matches found, try to find similar specialists
        if not service_matches:
            # Perform fuzzy matching on specialist names
            especialistas = Especialista.objects.filter(nombre__icontains=query)
            matches = [
                (especialista, fuzz.partial_ratio(query, especialista.nombre))
                for especialista in especialistas
            ]
            matches.sort(key=lambda x: x[1], reverse=True)  # Sort by similarity

            # Filter results to those with a similarity ratio above a certain threshold (adjust as needed)
            threshold = 50
            matches = [match[0] for match in matches if match[1] > threshold]

            if matches:
                # Retrieve services offered by the matched specialists
                servicios = Servicio.objects.filter(
                    especialistas__in=matches
                ).distinct()

            else:
                try:
                    precio = float(query)
                    servicios_ids = []
                    servicios = Servicio.objects.all()
                    for servicio in servicios:
                        servicio_precio = float(
                            get_precio_por_servicio(servicio.id)
                            .split(" ")[0]
                            .replace(",", ".")
                        )
                        if servicio_precio <= precio:
                            servicios_ids.append(servicio.id)

                    servicios = Servicio.objects.filter(id__in=servicios_ids)

                except ValueError:
                    message = "No  se encontraron servicios o especialistas que coincidan con la búsqueda."
                    return render(request, "home/home.html", {"message": message})

    for servicio in servicios:
        servicio.precio = get_precio_por_servicio(servicio.id)

    return render(request, "home/home.html", {"servicios": servicios})


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
