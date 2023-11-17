from django.contrib import admin

from .models import Servicio, Especialista, Invitado, Cita


class ServicioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion"]
    search_fields = ["nombre"]


admin.site.register(Servicio, ServicioAdmin)


class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    filter_horizontal = ["especialidades"]


admin.site.register(Especialista, EspecialistaAdmin)


class InvitadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono")

    search_fields = (
        "nombre",
        "email",
        "telefono",
    )


admin.site.register(Invitado, InvitadoAdmin)


class CitaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "invitado", "servicio", "especialista", "fecha")

    search_fields = (
        "usuario",
        "invitado",
        "servicio",
        "especialista",
        "fecha",
    )
    date_hierarchy = "fecha"


admin.site.register(Cita, CitaAdmin)
