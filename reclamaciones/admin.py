from django.contrib import admin
from .models import Reclamacion


class ReclamacionAdmin(admin.ModelAdmin):
    list_display = ("cita", "mensaje", "fecha")
    list_filter = ("cita", "fecha")
    search_fields = ("cita", "fecha")


admin.site.register(Reclamacion, ReclamacionAdmin)
