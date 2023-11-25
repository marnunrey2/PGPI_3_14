from django.shortcuts import render, redirect
from rest_framework.views import APIView


class AdminCitaView(APIView):
    def get(self, request):
        if request.user.is_staff:
            return render(request, "templates/admin_cita.html")
        else:
            return redirect("home:home")
