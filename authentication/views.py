from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm
from .serializers import UsuarioSerializer


# Non-api view
class LoginView(TemplateView):
    def post(self, request):
        form = LoginForm(request.POST)

        msg = None

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)
                    if request.user.is_staff:
                        return redirect("/admin_view/citas")
                    else:
                        return redirect("/")
                else:
                    msg = "Contraseña incorrecta"

            except User.DoesNotExist:
                msg = "Credenciales incorrectas"
        else:
            msg = "Error en el formulario"

        return render(request, "authentication/login.html", {"form": form, "msg": msg})

    def get(self, request):
        form = LoginForm(None)

        return render(request, "authentication/login.html", {"form": form, "msg": None})


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get("token", "")
        tk = get_object_or_404(Token, key=key)
        return Response(UsuarioSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("/")


class RegisterView(APIView):
    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect("/signin")
            except IntegrityError:
                # Handle the case where the user already exists
                error_message = "Usuario con este email ya existe"
                return render(
                    request,
                    "authentication/register.html",
                    {"form": form, "error_message": error_message},
                )
        else:
            return render(request, "authentication/register.html", {"form": form})

    def get(self, request):
        form = RegisterForm(None)
        return render(
            request, "authentication/register.html", {"form": form, "msg": None}
        )


class DeleteView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            userToDelete = User.objects.filter(id=request.user.id)
            userToDelete.delete()
            request.session.flush()
            success_message = "Su cuenta ha sido eliminada correctamente"
            return render(
                request, "home/home.html", {"success_message": success_message}
            )
        return redirect("/perfil")
