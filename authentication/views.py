from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.views import APIView

from .forms import LoginForm, RegisterForm
from .serializers import UserSerializer


# Non-api view
class LoginView(TemplateView):
    def post(self, request):
        form = LoginForm(request.POST)

        msg = None

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)

                return redirect("/")
            else:
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
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("/")


class RegisterView(APIView):
    def post(self, request):
        msg = None
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/signin")
        else:
            msg = form.errors
            return render(request, "authentication/register.html", {"form": form, "msg": msg})

    def get(self, request):
        form = RegisterForm(None)
        return render(
            request, "authentication/register.html", {"form": form, "msg": None}
        )