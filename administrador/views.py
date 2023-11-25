from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from citas.models import Cita
from django.contrib.auth.models import User


class AdminCitaView(APIView):
    def get(self, request):
        if request.user.is_staff:
            citas = Cita.objects.all()
            context = {"citas": citas}
            return render(request, "admin_cita.html", context)
        else:
            return redirect("home:home")
